from setuptools import setup

setup(name='lazypsf',
      version='4.3.1',
      description='A code for modelling PSFs and injecting fake sources with given flux distributions. Simulating Astro data',
      url= 'https://github.com/ryanc123/LazyPSF' ,
      author='Ry Cutter',
      author_email='R.Cutter@warwick.ac.uk',
      license='GNU',
      packages=['lazypsf'],
      package_data={'lazypsf': ['config/*.txt']},
      include_package_data=True,
      zip_safe=False)
