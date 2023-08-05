import os
from setuptools import setup

requirements = [
    "pymongo",
    "python-decouple==3.1",
    "redis==3.3.11",
    "numpy",
    "pandas",
    "pycrypto==2.6.1",
    "pymysql==0.9.3",
    "elasticsearch-dsl==6.3.1",
    "pika==0.12",
    "shortuuid==0.5.0",
    "requests==2.22.0",
    "threadpool==1.3.2",
    "python-dateutil==2.7",
    "sqlalchemy==1.2",
    'DBUtils==1.3'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='general-tools',
    version='0.2.6',
    packages=[
            "general_tools",
    ],
    license='BSD License',  # example license
    description='general tools',
    install_requires=requirements,
    long_description_content_type="text/markdown",
    url='',
    author='xw0102',
    author_email='15200813194@163.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)