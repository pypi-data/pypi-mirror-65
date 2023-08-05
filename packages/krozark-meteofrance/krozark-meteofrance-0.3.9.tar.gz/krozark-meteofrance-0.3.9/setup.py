from setuptools import setup

setup(
    name='krozark-meteofrance',
    version='0.3.9',
    description = 'Meteo-France weather forecast',
    author = 'victorcerutti',
    author_email = 'maxime.barbier1991+meteofrance@gmail.com',
    url = 'https://github.com/Krozark/meteofrance-py',
    packages=['meteofrance',],
    install_requires=[
       'requests',
       'beautifulsoup4',
       'pytz'
    ],
    license='MIT',
    long_description='Extract Meteo-France current weather and 1 hour rain forecast',
)
