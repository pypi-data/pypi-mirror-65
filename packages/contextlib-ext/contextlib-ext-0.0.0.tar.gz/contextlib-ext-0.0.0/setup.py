from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='contextlib-ext',
    version='0.0.0',
    description='Extensions for contextlib',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nikicat/contextlib-ext',
    author='Nikolay Bryskin',
    author_email='nbryskin@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='contextlib async development',
    packages=['contextlib_ext'],
    python_requires='>=3.7, <4',
    project_urls={
        'Bug Reports': 'https://github.com/nikicat/contextlib-ext/issues',
        'Source': 'https://github.com/nikicat/contextlib-ext/',
    },
)
