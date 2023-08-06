from setuptools import setup
from os import path
from io import open

classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Financial and Insurance Industry',
  'Programming Language :: Python',
  'Operating System :: OS Independent',
  'Natural Language :: English',
  'License :: OSI Approved :: MIT License'
]

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='bitvaluta_rpc',
      version='1.02',
      description='Library to communicate with bitvaluta daemon via JSON-RPC protocol.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/justluce/bitvaluta_rpc',
      author='justluce',
      author_email='support@justinluce.com',
      license='MIT',
      packages=['bitvaluta_rpc'],
      install_requires=['requests'],
      keywords=['bitvaluta', 'json-rpc', 'cryptocurrency', 'blockchain'],
      classifiers=classifiers,
      platforms="any")
