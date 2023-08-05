#!/usr/bin/env python

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='transformers_finetuning',  
     version='0.3.5',
     author="Ankur Singh",
     author_email="ankur310794@gmail.com",
     description="A Package for fine tuning based on transformers",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Ankur3107/transformers_finetuning",
     packages=['transformers_finetuning'],
     install_requires=['transformers','tensorflow','numpy'], 
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"
     ]
 )