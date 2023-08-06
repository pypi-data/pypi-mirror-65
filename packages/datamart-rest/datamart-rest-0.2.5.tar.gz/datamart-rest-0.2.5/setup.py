import io
import os
from setuptools import setup


os.chdir(os.path.abspath(os.path.dirname(__file__)))


with io.open('README.rst', encoding='utf-8') as fp:
    description = fp.read()
req = [
    'd3m',
    'datamart==2020.4.9',
    'requests',
    'websocket_client'
]
setup(name='datamart-rest',
      version='0.2.5',
      packages=['datamart_rest'],
      install_requires=req,
      description="Client library for DataMart's REST API",
      author="Remi Rampin, Fernando Chirigati",
      author_email='remi.rampin@nyu.edu, fchirigati@nyu.edu',
      maintainer="Remi Rampin, Fernando Chirigati",
      maintainer_email='remi.rampin@nyu.edu, fchirigati@nyu.edu',
      url='https://gitlab.com/datadrivendiscovery/datamart-api',
      project_urls={
          'Homepage': 'https://gitlab.com/datadrivendiscovery/datamart-api',
          'Source': 'https://gitlab.com/datadrivendiscovery/datamart-api',
          'Tracker': 'https://gitlab.com/datadrivendiscovery/datamart-api/issues',
      },
      long_description=description,
      license='BSD-3-Clause',
      keywords=['datamart', 'rest', 'auctus'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
          'Topic :: Scientific/Engineering :: Information Analysis'])
