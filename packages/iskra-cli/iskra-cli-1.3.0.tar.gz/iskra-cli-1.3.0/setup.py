import ast
from os.path import dirname, abspath
from setuptools import setup, find_packages


HERE = abspath(dirname(__file__))
README = open('README.md', encoding='utf-8').read()


tree = ast.parse(open('iskra.py').read())
for node in tree.body:
    if isinstance(node, ast.Assign) and node.targets[0].id == '__version__':
        version = node.value.s
        break

setup(
    name='iskra-cli',
    version=version,
    url='https://iskra.ml',
    author='Eddy Ernesto del Valle Pino',
    author_email='eddy@edelvalle.me',
    long_description=README,
    long_description_content_type='text/markdown',
    description="Let's you interact with Iskra from the terminal",
    license='Freeware',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.5',
    install_requires=[
        'httpx>=0.12.0,<0.13',
        'websockets==8.1',
        'colorama>=0.4,<0.5',
        'tqdm>=4,<5',
    ],
    scripts=['scripts/iskra'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
