import sys
import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = '0.0.5'
url = 'https://github.com/raeidsaqur/rsmlkit'

install_requires = [
    'numpy',
    'scipy',
    'networkx',
    'scikit-learn',
    'scikit-image',
    'requests',
    'plyfile',
    'pandas',
    'h5py'
]

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
setup_requires = [] + pytest_runner
tests_require = ['pytest', 'pytest-cov', 'mock']

setup(
    name="rsmlkit",
    version=__version__,
    author="Raeid Saqur",
    author_email="rsaqur@cs.princeton.edu",
    description="Auxialiary package for running experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        'machine learning',
        'data science',
        'research',
        'toolkit'
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    packages=find_packages(),
)