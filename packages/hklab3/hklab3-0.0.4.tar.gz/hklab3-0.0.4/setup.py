from setuptools import setup
import setuptools

setup(name="hklab3",
      version="0.0.4",
      url="http://github.com/kimhyokwan/hklab2",
      license="MIT",
      author="kimhyokwan",
      author_email="haiteam@kopo.ac.kr",
      keywords = ["calendar","isoweek","listsum"],
      description = "isoweek calculation and so on",
      packages=setuptools.find_packages(),
      install_requires=["isoweek"] 
     )