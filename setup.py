from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='backports.functools_partialmethod',
    version='3.5.1.0',
    description='Backport of functools.partialmethod from Python 3.5.1.',
    long_description=long_description,
    url='https://github.com/PythonBackports/backports.functools_partialmethod',
    author='Python Backports',
    author_email='pythonbackports@users.noreply.github.com',
    license='Python Software Foundation License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='python functools partialmethod backport',
    test_suite='tests',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)

