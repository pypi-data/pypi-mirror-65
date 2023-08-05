import codecs
import os
import sys

from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def get_definitions(rel_path, *words):
    dwords = {word: None for word in words}
    for line in read(rel_path).splitlines():
        for word in words:
            if line.startswith(f'__{word}__'):
                delim = '"' if '"' in line else "'"
                dwords[word] = line.split(delim)[1]
                break

    return [dwords[word] for word in dwords]


long_description = read('README.md')
base_folder = 'cache_gs'
packages = find_packages(where=base_folder)
_version, _description, _author, _author_email = get_definitions(
    os.path.join(base_folder, '__init__.py'),
    'version',
    'description',
    'author',
    'author_email')

setup(
    name='cache-guiosoft',
    version=_version,
    description=_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    url='https://github.com/guionardo/py-cache-guiosoft',
    keywords='cache',
    project_urls={
        "Documentation": "https://github.com/guionardo/py-cache-guiosoft/wiki",
        "Source": "https://github.com/guionardo/py-cache-guiosoft",
    },
    author=_author,
    author_email=_author_email,
    packages=find_packages(
        where=".",
        exclude=["tests"],
    ),

    install_requires=[
        "redis",
    ],
    zip_safe=True,
    python_requires='>=3.6.*'
)
