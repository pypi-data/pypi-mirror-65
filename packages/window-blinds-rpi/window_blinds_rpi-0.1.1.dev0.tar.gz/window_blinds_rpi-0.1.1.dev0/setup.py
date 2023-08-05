from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.rst')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'window_blinds_rpi', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='window_blinds_rpi',
    version=version['__version__'],
    description=('Show how to structure a Python project.'),
    long_description=long_description,
    author='Tine Živič',
    author_email='tine.zivic@gmail.com',
    url='https://github.com/tinezivic/window_blinds_rpi',
    license='MPL-2.0',
    packages=['window_blinds_rpi'],
#   no dependencies in this example
    install_requires=[

        'pandas' , 'RPi.GPIO', 'time', 'asycio', 'bitstring', 'smbus2'
    ],
#   no scripts in this example
#   scripts=['bin/a-script'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
)
