from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="anyrun",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'websocket_client==0.56.0',
        'pytest-runner==5.1'
    ],
    tests_require=[
        'pytest==4.6.2',
        'pytest-cov==2.7.1',
        'codecov==2.0.15',
        'prospector==1.1.6.2',
    ],
    package_data={
        '': ['*.txt', '*.md'],
    },
    zip_safe=False,

    author="Michal Walkowski",
    author_email="mi.walkowski@gmail.com",
    description="app.any.run malware submissions client",
    long_description=long_description,
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
