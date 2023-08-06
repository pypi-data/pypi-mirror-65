#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fjmvlib", # Replace with your own username
    packages=['fjmvlib'],
    version="0.5",
    author="Oxana Sannikova",
    author_email="osanniko@cisco.com",
    description="A small package with helper functions to validate Fire Jumper Programmability Mission submissions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oxsannikova/fjmvlib",
    download_url="https://github.com/oxsannikova/fjmvlib/archive/v_05.tar.gz",
    #install_requires=[            
    #      'requests',
    #      'json',
    #  ],
    #packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)