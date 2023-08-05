from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='mserv',
    author='Quinton',
    version='0.3',
    scripts=['mserv.py'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='An attempt at a Minecraft server manager',
    url='https://github.com/mexiquin/mserv'
)