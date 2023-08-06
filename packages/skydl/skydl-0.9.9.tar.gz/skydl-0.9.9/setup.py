import os
import codecs
import skydl
from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_install_requires():
    with open('requirements.txt', 'r') as f:
        res = f.readlines()
    res = list(map(lambda s: s.replace('\n', ''), res))
    return res


setup(
    name='skydl',
    version=skydl.__version__,
    description="",
    long_description=readme,
    install_requires=read_install_requires(),
    setup_requires=['setuptools>=41.0.1', 'wheel>=0.33.4'],
    author='tony',
    author_email='',
    license='BSD',
    url='',
    keywords=['robot', 'ai', 'reinforcement learning', 'machine learning', 'RL',
              'ML', 'tensorflow', 'pytorch', 'ray', 'skydl', 'high efficiency', 'deep learning'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'],
    packages=find_packages(exclude=[]),
    package_data={'': []},
)