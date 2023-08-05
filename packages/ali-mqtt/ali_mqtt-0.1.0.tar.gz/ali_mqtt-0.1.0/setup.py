#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages
import ali_mqtt as m

setup(
    name='ali_mqtt',
    version=m.__version__,
    description='MQTT auth info generator for Ali IoT',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author='IvanLuLyf',
    author_email='me@ivanlu.cn',
    url='https://github.com/twimicn/ali-mqtt',
    py_modules=['ali_mqtt'],
    scripts=['ali_mqtt.py'],
    license='MIT',
    platforms='any',
    classifiers=['Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 ],
)
