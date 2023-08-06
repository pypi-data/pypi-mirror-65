import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   name="simple-common-utils",
   version="0.0.2",
   author="Ruben Shalimov",
   author_email="r_shalimov@inbox.ru",
   description="Common utils for python3 projects.",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/RobinBobin/python3-common-utils",
   packages=setuptools.find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent"
   ]
)
