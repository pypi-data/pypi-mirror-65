from setuptools import setup
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name='bee_data_api',
      version='0.5',
      description='For working with api methods of the test environment',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['bee_data_api'],
      author='steep_11',
      author_email='steep1183@gmail.com',
      zip_safe=False,
      install_requires=['requests'])
