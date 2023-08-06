#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='sentry-wechat-plugin-renew',
    version='1.0.1',
    keywords='sentry wechat ',
    author='cxt',
    author_email='cxt1122jk@gmail.com',
    url='https://github.com/susujs/sentry-wechat-plugin.git',
    description='A Sentry extension which integrates with Wechat robot.',
    long_description='A Sentry extension which integrates with Wechat robot',
    long_description_content_type="text/markdown",
    license='BSD',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        'sentry>=9.0.0',
        'requests',
        'pytz',
        'django',
    ],
        entry_points={
        'sentry.plugins': [
            'wechat = sentry_wechat.plugin:WechatPlugin'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)