from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
	name='jb4jupyter',
	version='0.1',
	description='jupyter beautifier by @jb4earth',
	url='http://gitlab.com/jb4earth/jb4jupyter',
	author='@jb4earth',
	author_email='jb4earth@gmail.com',
	license='GPL',
	packages=find_packages(),
	long_description=long_description,
    long_description_content_type="text/markdown"
	)
