import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
	name= "calc-project",
	version="1.0.0",
	author="Pragnya Rout",
	author_email="pragnyarout2018@gmail.com",
	description="A simple package calculating value",
	long_description=long_description,
    long_description_content_type="text/markdown",

	url="",
	keywords='package numbers calculations',

	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 2",
		"Operating System :: OS Independent"
	],
	)
