#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup

with open("README.md","r") as fh:
    ld = fh.read()

setup(
    name='geot_cluster',
    version='0.9.20',
    description='Reasearch project on clustering clients from transaction history',
    author='Korsakov Aleksandr',
    author_email='corsakov.alex@yandex.ru',
    url='https://github.com/LarsWallenstein/Geotrans_cluster',
    py_modules=["geot_cluster"],
    package_dir={'':'src'},
    long_description = ld,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

