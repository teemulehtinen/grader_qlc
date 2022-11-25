"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readmefile_contents = f.read()

setup(
    name='grader_qlc',
    version='1.0.0',
    description='Allows augmenting existing programming submissions with QLCs',
    long_description=readmefile_contents,
    url='https://github.com/teemulehtinen/grader_qlc',
    author='Teemu Lehtinen',
    author_email='teemu.t.lehtinen@aalto.fi',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyYAML ~= 6.0',       # Parse configuration files
    ],
    entry_points={
        'console_scripts': ['qlc_wrap = grader_qlc:qlc_wrap']
    }
)