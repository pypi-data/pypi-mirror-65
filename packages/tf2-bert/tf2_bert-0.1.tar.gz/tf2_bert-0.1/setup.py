from setuptools import setup
from setuptools import find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'tf2_bert',      
    version = '0.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'QinBingFeng',        
    author_email = '114479602@qq.com',
    url = 'https://github.com/Qinbf/tf2_bert',
    description = 'tf2_bert',
    packages=find_packages()
    )