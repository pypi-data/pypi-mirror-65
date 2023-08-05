from setuptools import setup, find_packages

with open("README.md", 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='mserv',
    author='Quinton',
    version='0.5',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='An attempt at a Minecraft server manager',
    url='https://github.com/mexiquin/mserv',
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=requirements,
        entry_points={
        'console_scripts':[
            'mserv=mserv.mserv:main'
        ]
    }
)