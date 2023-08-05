import setuptools


setuptools.setup(
    name='bingy',
    version='0.1.0',

    packages=['bingy', 'bingy.aio'],
    install_requires=['bs4', 'urllib3', 'aiohttp', 'certifi'],

    url='https://github.com/AmanoTeam/bingpy',

    author='Amano Team',
    author_email='contact@amanoteam.com',

    license='MIT',

    description='A simple module for searching on DuckDuckGo',
    long_description='',
    long_description_content_type='text/markdown'
)