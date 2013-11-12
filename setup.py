from distutils.core import setup

setup(
    name='noaaweather',
    version='0.1.0',
    author='Matthew Howland',
    author_email='matt.howland@lab45.com',
    packages=['noaaweather', 'noaaweather.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/noaaweather/',
    license='LICENSE.txt',
    description='Easy use of NOAA weather services.',
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4>=4.3.2",
        "iso8601>=0.1.8",
    ],
)