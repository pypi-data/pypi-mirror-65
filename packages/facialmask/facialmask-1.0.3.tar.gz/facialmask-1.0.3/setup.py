#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['Click>=7.0', 'numpy', 'pillow', 'opencv-python']

setup(
    author="Devin C. Horvay",
    author_email='devin.c.horvay@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Pixelate faces automatically classified in images through a Python CLI.",
    entry_points={
        'console_scripts': [
            'facialmask=facialmask.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='facialmask pixelate facedetection face',
    name='facialmask',
    packages=find_packages(include=['facialmask', 'facialmask.*']),
    url='https://github.com/dhorvay/facial-mask',
    version='1.0.3',
    zip_safe=False,
)
