from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='clickandcollectnz',
      version='0.1.1',
      description='A package to get information about Click and Collect slots in NZ',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/jesserockz/python-clickandcollectnz',
      author='Jesse Hills',
      license='MIT',
      install_requires=['requests', 'beautifulsoup4'],
      packages=find_packages(exclude=["dist"]),
      zip_safe=True)
