from setuptools import setup

setup(name="hklab3",
      version="0.0.2",
      url="http://github.com/kimhyokwan/hklab2",
      license="MIT",
      author="kimhyokwan",
      author_email="haiteam@kopo.ac.kr",
      keywords = ["calendar","isoweek","listsum"],
      description = "isoweek calculation and so on",
      packages=["hklab2","hklab3"],
      install_requires=["isoweek"] 
     )