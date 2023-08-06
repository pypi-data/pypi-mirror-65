import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   author="Ruben Shalimov",
   author_email="r_shalimov@inbox.ru",
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent"
   ],
   description="Common utils for python3 projects.",
   long_description=long_description,
   long_description_content_type="text/markdown",
   name="simple-common-utils",
   packages=setuptools.find_packages(),
   url="https://github.com/RobinBobin/python3-common-utils",
   version="0.0.4"
)
