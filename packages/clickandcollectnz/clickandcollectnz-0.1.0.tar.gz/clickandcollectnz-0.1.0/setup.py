from setuptools import setup, find_packages

setup(name='clickandcollectnz',
      version='0.1.0',
      description='',
      url='http://github.com/jesserockz/python-clickncollect',
      author='Jesse Hills',
      license='MIT',
      install_requires=['requests'],
      packages=find_packages(exclude=["dist"]),
      zip_safe=True)
