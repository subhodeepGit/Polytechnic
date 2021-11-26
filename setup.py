from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in polytechnic/__init__.py
from polytechnic import __version__ as version

setup(
	name="polytechnic",
	version=version,
	description="SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED",
	author="SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED",
	author_email="soul@soulunileaders.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
