
"""Setup for the hyperpy package."""

import setuptools

with open('DESCRIPION.rst') as f:
    README = f.read()

requirements_f = open('requirements.txt', 'r')
dependencies = [ req for req in requirements_f.readlines() ]
exec(open('hyperpy/_version.py').read())
setuptools.setup(
    author="Sunny Arya",
    version=__version__,
    author_email="sunnyiniari@gmail.com",
    name='hyperpy',
    license="MIT",
    platforms=['Any'],
    description="hyperpy: Scientific python library for Hyperspectral plant phenotyping and image processing.",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://hyperpy.readthedocs.io/en/latest/',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=dependencies,
    keywords='plant phenotyping Hyperspectral Remote Sensing bioinformatics ',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
