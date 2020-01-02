import os
import sys
from setuptools import setup, find_packages


assert sys.version_info >= (3, 3), 'Python 3.3+ required.'

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def read(file_name):
    return open(os.path.join(THIS_DIRECTORY, file_name), encoding='utf-8').read()


def install_requires():
    return read('requirements.txt').splitlines()


def tests_require():
    return read('test_requirements.txt').splitlines()

setup(
    name="anyrun",
    version="0.3",
    packages=find_packages(),
    install_requires=install_requires(),
    tests_require=tests_require(),
    package_data={
        '': ['*.txt', '*.md'],
    },
    zip_safe=False,

    author="Michal Walkowski",
    author_email="mi.walkowski@gmail.com",
    description="app.any.run malware submissions client",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license="pache Software License 2.0",
    keywords="malware submissions app.any.run",
    url="https://github.com/mwalkowski/anyrun",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
