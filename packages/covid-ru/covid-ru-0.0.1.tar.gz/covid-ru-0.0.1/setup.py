# coding=utf-8
from setuptools import setup

setup(
    name='covid-ru',
    version='0.0.1',
    packages=['covid_ru'],
    url='https://github.com/strizhechenko/covid-ru',
    license='MIT',
    author='Oleg Strizhechenko',
    author_email='oleg.strizhechenko@gmail.com',
    description='Getting latest covid-19 stats in Russia to your cli',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Public Domain',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'covid-ru=covid_ru.__init__:main',
        ],
    },
)
