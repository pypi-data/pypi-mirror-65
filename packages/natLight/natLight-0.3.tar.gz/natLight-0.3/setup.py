from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name='natLight',
	version='0.3',
	description='Natural Ligth to RGB Converter',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://gitlab.com/stroblme/naturalLight.git',
	author='Melvin Strobl',
	packages=find_packages(),
	python_requires='>=3.6'
)