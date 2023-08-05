#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup

setup(name = 'solWeek',
     version = '0.0.1',
     url = 'https://github.com/sol-91/pyPackage',
     license = 'MIT',
     author = 'solhan',
     author_email = 'sky910829@naver.com',
     keywords = ['calendar', 'yearweek'],
     description = 'Fintech API',
     packages = ['solWeek'],
     install_requires = ['isoweek'])

