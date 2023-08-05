import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = '0.0.1'
url = 'https://github.com/raeidsaqur/rsmlkit'

install_requires = [
    'torch',
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

setup_requires = ['pytest-runner']
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
    python_requires='>=3.6',
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    packages=find_packages(),
)