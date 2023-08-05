from setuptools import setup
import os

ROOT_DIR='pylatlon'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pylatlon',
      version=version,
      description='Tools to handle geographic positions (parsing, gui input)',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='https://github.com/MarineDataTools/pylatlon',
      author='Peter Holtermann',
      author_email='peter.holtermann@io-warnemuende.de',
      license='GPLv03',
      packages=['pylatlon'],
      scripts = [],
      entry_points={},
      install_requires=[ 'pyproj'],
      package_data = {'':['VERSION']},
      ython_requires='>=3.4',
      zip_safe=False)


