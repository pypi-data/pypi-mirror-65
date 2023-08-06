from setuptools import setup, find_packages
 
setup(
	name = "datahubsdk",
	version = "1.02",
	author = "zhangyuhao25@jd.com",
	author_email = "zhangyuhao25@jd.com",
	url = 'http://git.jd.com/datahub/dataopssdk.git',
	long_description = open('README.md').read(),
	packages = ["sdktool","sdktool.util"]
)
