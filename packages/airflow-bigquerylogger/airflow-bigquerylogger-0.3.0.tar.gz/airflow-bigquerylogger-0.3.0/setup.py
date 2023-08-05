#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
   long_description = fh.read()

with open('requirements.txt') as f:
   requires = f.readlines()

setup(
   name='airflow-bigquerylogger',
   version='0.3.0',
   description='BigQuery logger handler for Airflow',
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Gabriele Diener',
   author_email='gabriele.diener@gmail.com',
   install_requires=requires,
   packages=find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   python_requires='>=3.6'
)

