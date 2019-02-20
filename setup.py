from distutils.core import setup

setup(
    name='py-synology',
    version='0.3.0',
    packages=['synology'],
    url='https://github.com/snjoetw/py-synology',
    license='MIT',
    author='snjoetw',
    author_email='snjoetw@gmail.com',
    description='Python API for Synology Surveillance Station',
    requires=['requests']
)
