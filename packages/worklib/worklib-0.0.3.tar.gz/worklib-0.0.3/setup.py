#-*- coding:utf-8 -*-
import setuptools

with open("README.md","r") as file:
	long_description = file.read()

setuptools.setup(
	name="worklib",
	version="0.0.3",
	author="lzh",
	author_email="743872668@qq.com",
	description=long_description,
	long_description_content_type="text/markdown",
	url="",
	packages=setuptools.find_packages(),
	classfiers=[""]

)
