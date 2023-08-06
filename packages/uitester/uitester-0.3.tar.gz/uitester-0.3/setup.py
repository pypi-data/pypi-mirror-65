import codecs
import os
import sys
try:
  from setuptools import setup,find_packages
except:
  from distutils.core import setup

def read(fname):
  return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name = "uitester",
  version = "0.3",
  description = "package description.",
  long_description = read("README.rst"),
  classifiers =  ['License :: OSI Approved :: MIT License','Programming Language :: Python','Intended Audience :: Developers','Operating System :: OS Independent'],
  keywords = "web ui autotest python package",
  author = "gaianote311",
  author_email = "gaianote311@gmail.com",
  url = "http://gaianote.github.io/",
  license = "MIT",
  packages = find_packages(),
  include_package_data=True,
  package_data = {'uitester':['javascript/*','bin/*/*/*/*','bin/*/*/*','bin/*/*','bin/*']},
  zip_safe=True,
  install_requires = ["selenium","fire","pytest","browsermob-proxy"],
  entry_points={
        'console_scripts':[
        'uitester = uitester:cli'
    ]}
)
