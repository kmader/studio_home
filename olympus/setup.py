from setuptools import setup, find_packages


setup(
  name = 'olympus',
  version = '0.41',
  description = 'A tool for creating a REST API for any machine learning model, in seconds.',
  author = 'Galiboo',
  author_email = 'hello@galiboo.com',
  url = 'https://github.com/galiboo/olympus', # use the URL to the github repo
  download_url = 'https://github.com/galiboo/olympus/archive/0.41.tar.gz', 
  py_modules=['olympus'],
  keywords = ['machine learning', 'python', 'rest', 'api', 'deep learning'],
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python'
  ],
  entry_points={
  'console_scripts': [
    'olympus = olympus.olympus:cli'
    ]
  },
  install_requires=[
  "click==6.6",
  "haikunator==2.1.0",
  "prettytable==0.7.2",
  "tinydb==3.7.0"],
)