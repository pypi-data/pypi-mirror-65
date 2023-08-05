from distutils.core import setup
setup(
  name = 'MLgeometry',
  packages = ['MLgeometry', 'MLgeometry.geometries'],
  version = '0.1.3',
  license= '',
  description = 'Package for representing data as Objects with common geometries. Used as an interface for prediction elements in Computer Vision problems',
  author = 'Juan Carlos Arbeláez',
  author_email = 'juanarbelaez@vaico.com.co',
  url = 'https://jarbest@bitbucket.org/jarbest/mlgeometry.git',
  download_url = 'https://bitbucket.org/jarbest/mlgeometry/get/master.tar.gz',
  keywords = ['vaico', 'geometry', 'ml'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ]
)