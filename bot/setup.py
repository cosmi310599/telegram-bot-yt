from setuptools import setup, find_packages

setup(
    name='pyvideo_bot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'telebot',
        'yt_dlp',
    ],
)
