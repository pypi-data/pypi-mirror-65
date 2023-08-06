from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cha_dist',
version='0.4',
 description='Gaussian distributions',
 packages=['cha_dist'],
 author='Nagesh Singh Chauhan',
 author_email='nageshsinghc4@gmail.com',
 long_description=long_description,
    long_description_content_type='text/markdown'
 ,zip_safe=False)