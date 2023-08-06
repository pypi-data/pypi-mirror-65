#! /usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools

setup(
    name='restsql',  # 包的名字
    author='venzo',  # 作者
    version='0.1.0',  # 版本号
    license='MIT',

    description='restsql python',  # 描述
    long_description='''restsql python''',
    author_email='594948794@qq.com',  # 你的邮箱**
    url='',  # 可以写github上的地址，或者其他地址
    # 包内需要引用的文件夹
    # packages=setuptools.find_packages(exclude=['url2io',]),
    packages=["src"],
    # 依赖包
    install_requires=[
        'certifi==2019.9.11',
        'chardet==3.0.4',
        'elasticsearch==5.4.0',
        'elasticsearch-dsl==5.3.0',
        'guppy==0.1.10',
        'idna==2.8',
        'ipaddress==1.0.23',
        'mysqlclient==1.4.2.post1',
        'numpy==1.16.5',
        'pandas==0.24.2',
        'psycopg2-binary==2.8.4',
        'pycrypto==2.6.1',
        'python-dateutil==2.8.0',
        'pytz==2019.2',
        'requests==2.22.0',
        'six==1.12.0',
        'urllib3==1.25.6'
    ],
    classifiers=[
        # 'Development Status :: 4 - Beta',
        # 'Operating System :: Microsoft'  # 你的操作系统  OS Independent      Microsoft
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        # 'License :: OSI Approved :: BSD License',  # BSD认证
        'Programming Language :: Python',  # 支持的语言
        'Programming Language :: Python :: 2.7',  # python版本 。。。
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)