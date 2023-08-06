import re

from setuptools import setup


version = ''
with open('omeku/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


if not version:
    raise RuntimeError('version is not set')


setup(
    name='omeku.py',
    author='jdev2005',
    url='https://github.com/jdev2005/omeku.py',
    version=version,
    packages=['omeku'],
    license='MIT',
    description='A Python module that uses Omeku API',
    include_package_data=True,
    install_requires=requirements
)
