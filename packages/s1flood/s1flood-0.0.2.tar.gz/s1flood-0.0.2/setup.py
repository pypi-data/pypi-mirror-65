from setuptools import setup
import os
import ee

ee.Initialize()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

exec(read('s1flood/__version__.py'))

setup(
    name = 's1flood',
    version = __version__,
    packages = ['s1flood',],
    license = 'MIT',
    long_description = read('README.md'),
    long_description_content_type='text/markdown',
    install_requires = [
        'earthengine_api',
        'httplib2shim'
        ],
    author = 'Ben DeVries',
    author_email = 'bdv@uoguelph.ca',
    url = 'https://github.com/bendv/s1flood'
)

try:
    import eedswe
except ImportError:
    print(f'\033[93m', "The `eedswe` package is optional, but needed to include historical DSWE in flood maps. JRC Global Surface Water data will be used alone in its absence.", sep = '')
    print("Go to https://github.com/bendv/eedswe for instructions on how to install eedswe", f'\033[0m', sep = '')

