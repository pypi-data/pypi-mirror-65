
"""Setup for the hyperpy package."""

import setuptools

# his opens he descripion file 
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
    description='hyperpy a python package for Hyperspecral phenoyping and hyperspecral image processing.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=dependencies,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries',
    ],
)