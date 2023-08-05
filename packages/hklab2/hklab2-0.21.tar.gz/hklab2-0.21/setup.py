from setuptools import setup

setup(name="hklab2",
      version="0.21",
      url="http://github.com/kimhyokwan/hklab2",
      license="MIT",
      author="kimhyokwan",
      author_email="haiteam@kopo.ac.kr",
      keywords = ["calendar","isoweek","listsum"],
      description = "isoweek calculation and so on",
      packages=["hklab2"],
      install_requires=["isoweek"] 
     )