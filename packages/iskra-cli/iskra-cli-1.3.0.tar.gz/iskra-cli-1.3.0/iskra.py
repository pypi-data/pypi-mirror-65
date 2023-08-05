#!/usr/bin/env python

import asyncio
import json
import logging
import sys
import webbrowser
import os
import functools
from os import environ as env
from os.path import isfile, isdir, exists, join, basename
from glob import glob
from pathlib import Path
from subprocess import check_output, CalledProcessError, DEVNULL

import colorama
from tqdm import tqdm

import httpx
from httpx._content_streams import AsyncIteratorStream

import websockets
from websockets.exceptions import ConnectionClosedOK


__version__ = '1.3.0'

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG if '--debug' in sys.argv else logging.INFO)
logger.addHandler(logging.StreamHandler())

MEGA_BYTE = 1024 ** 2
MINUTE = 60


def sync_to_async(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        p_func = functools.partial(fn, *args, **kwargs)
        return await loop.run_in_executor(None, p_func)
    return wrapper


class WebSocketClient:

    async def loop(self):
        try:
            async with websockets.connect(
                self.websocket_url,
                max_size=2 * MEGA_BYTE,
                ping_interval=5 * MINUTE,
                ping_timeout=5 * MINUTE,
            ) as ws:
                self.ws = ws
                await self.on_open()
                while await self.on_message():
                    pass
        finally:
            await self.on_close()

    async def on_open(self):
        pass

    async def on_message(self):
        try:
            message = await self.ws.recv()
        except ConnectionClosedOK:
            return False

        message = json.loads(message)
        message_type = message.pop('type', None)
        handler = getattr(self, 'receive_' + message_type, None)
        if handler:
            await handler(**message)
            return True
        else:
            await self.receive_print(
                [
                    'Did not understand message from server:',
                    message_type,
                    message
                ],
                {'color': 'RED'}
            )
            return False

    async def on_close(self):
        pass

    # Data transmission

    async def send(self, **kwargs):
        await self.ws.send(json.dumps(kwargs))

    async def send_bytes(self, data):
        await self.ws.send(data)

    async def receive(self):
        return json.loads(await self.ws.recv())

    # Receivers

    async def receive_print(self, args, kwargs):
        color = kwargs.pop('color', None)
        if color:
            color = color and getattr(colorama.Fore, color, None)
            print(
                color + colorama.Style.BRIGHT + ':: ',
                end=colorama.Style.RESET_ALL
            )
        print(*args, **kwargs)


class Iskra(WebSocketClient):
    def __init__(
        self,
        host,
        argv,
        ws_path='/api/cli',
        upload_path='/upload',
    ):
        if host.startswith('localhost'):
            ws_schema = 'ws://'
            http_schema = 'http://'
        else:
            ws_schema = 'wss://'
            http_schema = 'https://'

        self.host = host
        self.ws_schema = ws_schema
        self.http_schema = http_schema
        self.ws_path = ws_path
        self.upload_path = upload_path
        self.argv = argv
        self.read_configuration()

    @property
    def websocket_url(self):
        return self.ws_schema + self.host + self.ws_path

    @property
    def upload_url(self):
        return self.http_schema + self.host + self.upload_path

    async def loop(self):
        command = self.argv[:1]

        # Dispatch local command
        if command:
            command_handler = getattr(self, 'cmd_' + command[0], None)
            if command_handler:
                await command_handler(*sys.argv[2:])
                return

        # Send to iskra
        await super().loop()

    # Configuration

    def get_config(self, keys, defalut=None):
        value = self.config
        for key in keys.split('.'):
            value = value.get(key) or {}
        return value or defalut

    def read_configuration(self):
        self.config_dir = Path.home().joinpath('.iskra')
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir.joinpath('config.json')
        self.config_file.touch()
        self.config = json.loads(self.config_file.read_text() or '{}')

    def write_configuration(self, **kwargs):
        self.config = kwargs
        self.config_file.write_text(json.dumps(self.config, indent=4))

    # WebSocket event handlers

    async def on_open(self):
        await self.run_command()

    async def run_command(self, *argv):
        await self.send(type='command', argv=self.argv)

    # Local commands

    async def cmd_logout(self):
        self.config.pop('jwt', None)
        self.write_configuration()
        await self.receive_print(['Bye bye...'], {'color': 'GREEN'})

    # Receivers

    async def receive_jwt(self, refresh, access):
        self.write_configuration(jwt={
            'refresh': refresh,
            'access': access,
        })

    async def receive_machine(self, host, command, argv):
        self.talk_to_server = type(self)(
            host, argv,
            ws_path='/cli/' + command,
            upload_path='/upload',
        )

    async def receive_open_browser(self, url):
        webbrowser.open(url)

    async def receive_write_metadata(self, **kwargs):
        file = Path.cwd().joinpath('.iskra.json')
        file.write_text(json.dumps(kwargs))

    # Responders

    async def receive_prompt(self, request_id, msg):
        value = await sync_to_async(input)(msg + ': ')
        await self.send(request_id=request_id, value=value)

    async def receive_send_access_token(self, request_id=None):
        access_token = self.get_config('jwt.access', '')
        await self.send(access_token=access_token, request_id=request_id)

    async def receive_send_refresh_token(self, request_id):
        refresh_token = self.get_config('jwt.refresh', '')
        await self.send(refresh_token=refresh_token, request_id=request_id)

    async def receive_send_metadata(self, request_id):
        conf_file = Path.cwd().joinpath('.iskra.json')
        if not conf_file.exists():
            conf_file.write_text(json.dumps({'name': Path.cwd().name}))
        conf = json.loads(conf_file.read_text())
        await self.send(**dict(conf, request_id=request_id))

    async def receive_send_env_metadata(self, request_id):
        await self.send(env_metadata=get_env_metadata(), request_id=request_id)

    async def receive_dir_size(self, request_id):
        metadata = get_local_files_metadata()
        total_size = sum(f['size'] for f in metadata)
        await self.send(total_size=total_size, request_id=request_id)

    # File transfers:

    async def receive_start_file_transfer(self, upload_path=None):
        self.upload_path = upload_path or self.upload_path
        metadata = get_local_files_metadata()
        total_size = sum(f['size'] for f in metadata)
        progress = tqdm(
            total=total_size,
            desc='Sync',
            unit='b',
            unit_scale=True,
            unit_divisor=1024,
        )
        headers = {
            'Authorization': 'JWT ' + self.config['jwt']['access']
        }
        async with httpx.AsyncClient(
            http2=True,
            headers=headers,
            base_url=self.upload_url
        ) as client:
            for files in slicing_window(metadata):
                await self.send(
                    type='files',
                    files=[
                        [f['path'], f['size'], f['mtime_ns']]
                        for f in files
                    ]
                )
                paths_to_send = await self.receive()
                for file in files:
                    if file['path'] in paths_to_send:
                        await self.upload_file(progress, client, file)
                    else:
                        progress.update(file['size'])

        with progress:
            progress.close()

        await self.send(type='EOT')

    async def upload_file(self, progress, client: httpx.AsyncClient, file):
        # HACK: stream the file upload
        #   - is async, so it does not block the websocket ping
        #   - updates the progress granularly
        #   - does not http timeout
        request = client.build_request(
            method='POST',
            url=file['path'],
            headers={'x-mtime-ns': str(file['mtime_ns'])},
            files={'file': open(file['path'], 'rb')},
        )
        data_stream = request.stream.body

        progress.total += len(data_stream) - file['size']

        async def stream():
            for chunk in slicing_window(data_stream, size=MEGA_BYTE):
                progress.update(len(chunk))
                yield chunk

        request.stream = AsyncIteratorStream(stream())
        response = await client.send(request)
        response.raise_for_status()


# Introspection

@functools.lru_cache()
def get_local_files_metadata():
    metadata = []
    paths = glob('**', recursive=True)
    dirs_to_ignore = set()
    for path in tqdm(paths, desc="Checksum", unit='file'):
        if any(path.startswith(d) for d in dirs_to_ignore):
            continue

        ignore_this = (
            isdir(path) and (
                basename(path) in ('__pycache__', '.git') or
                exists(join(path, 'bin', 'activate')) or
                exists(join(path, '.iskra.json'))
            )
        )
        if ignore_this:
            dirs_to_ignore.add(path)
            continue

        if isfile(path):
            stat = os.stat(path)
            metadata.append({
                'path': path,
                'size': stat.st_size,
                'mtime_ns': stat.st_mtime_ns,
            })
    return metadata


def get_env_metadata():
    data = {'cwd': os.getcwd()}
    try:
        return dict(
            data,
            conda=check_output(
                ['conda', 'env', 'export'],
                stderr=DEVNULL
            ).decode(),
        )
    except (FileNotFoundError, CalledProcessError):
        major, minor, *_ = sys.version_info
        return dict(
            data,
            pip={
                'python': str(major) + '.' + str(minor),
                'requirements': check_output(['pip', 'freeze']).decode(),
            }
        )


def slicing_window(iterable, size=5):
    start = 0
    while iterable[start:start + size]:
        yield iterable[start:start + size]
        start += size


async def main():
    try:
        data = httpx.get('https://pypi.org/pypi/iskra-cli/json').json()
    except Exception:
        pass
    else:
        if data['info']['version'] != __version__:
            print(
                colorama.Back.RED +
                colorama.Fore.BLACK +
                "!! You are using an outdated iskra-cli, ugrade:" +
                colorama.Style.RESET_ALL
            )
            print()
            print("    pip install --upgrade iskra-cli")
            print()

    iskra = Iskra(
        host=env.get('ISKRA_HOST', 'app.iskra.ml'),
        argv=sys.argv[1:]
    )
    while iskra:
        await iskra.loop()
        iskra = getattr(iskra, 'talk_to_server', None)


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
