import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="mkcloud",
  version="0.0.1",
  author="makeblock",
  author_email="tongsen@makeblock.com",
  description="a little chat bot",
  long_description=long_description,
  url="https://github.com/pypa/mkcloud",    
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  platforms = 'any',
  install_requires = ['json','requests'],
)