import sys
import os

from setuptools import find_packages
from distutils.core import setup
 
if sys.argv[-1] == 'publish':
  os.system('python setup.py sdist bdist_wheel')
  os.system('twine upload dist/*')
  sys.exit()
if sys.argv[-1] == 'clean':
  os.system('rm -rf dist')
  os.system('rm -rf build')
  os.system('rm -rf pygame_dashboard.egg-info')

setup(name='pygame_dashboard',
      version='0.0.1',
      url='https://github.com/brunosantanaa/pygame-dashboard',
      license='MIT',
      author='Bruno Santana',
      author_email='bruno.sant.a@gmail.com',
      description='Simples elements of Dashboard from PyGame',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)