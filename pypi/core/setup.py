from setuptools import setup, find_packages
import coppertop.core

# read the contents of README.md file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = coppertop.core.version

# print(find_packages())


setup(
  name='coppertop',
  packages=[
    'bones',
    'bones.core',
    'bones.tests',
    'coppertop',
    'coppertop._structs',
    'coppertop.std',
    'coppertop.std._linalg',
    'coppertop.std._stats',
    'coppertop.std.tests',
    'coppertop.tests',
  ],
  # package_dir = {'': 'core'},
  # namespace_packages=['coppertop_'],
  version=version,
  python_requires='>=3.8',
  license='BSD',
  description = 'Some batteries Python didn\'t come with',
  long_description_content_type='text/markdown',
  long_description=long_description,
  author = 'David Briant',
  author_email = 'dangermouseb@forwarding.cc',
  url = 'https://github.com/DangerMouseB/coppertop',
  download_url = '',
  # download_url = f'https://github.com/DangerMouseB/coppertop/archive/{version}.tar.gz',
  keywords = ['piping', 'pipeline', 'pipe', 'functional'],
  install_requires=[],
  include_package_data=True,
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'Topic :: Utilities',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  zip_safe=False,
)
