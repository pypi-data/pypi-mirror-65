import io
import os
from setuptools import setup


os.chdir(os.path.abspath(os.path.dirname(__file__)))


with io.open('README.rst', encoding='utf-8') as fp:
    description = fp.read()
req = [
    'datamart-rest==0.2.5',
]
setup(name='datamart-nyu',
      version='0.2.5',
      py_modules=['datamart_nyu'],
      install_requires=req,
      description="Client library for NYU's DataMart system",
      author="Remi Rampin, Fernando Chirigati",
      author_email='remi.rampin@nyu.edu, fchirigati@nyu.edu',
      maintainer="Remi Rampin, Fernando Chirigati",
      maintainer_email='remi.rampin@nyu.edu, fchirigati@nyu.edu',
      url='https://gitlab.com/ViDA-NYU/datamart/datamart-api',
      project_urls={
          'Homepage': 'https://gitlab.com/ViDA-NYU/datamart/datamart-api',
          'Source': 'https://gitlab.com/ViDA-NYU/datamart/datamart-api',
          'Tracker': 'https://gitlab.com/ViDA-NYU/datamart/datamart-api/issues',
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
