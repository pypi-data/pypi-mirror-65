from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='github-sectory',
	version='1.2.1',
	description='CLI for downloading sub-directory of any Github repository!',
	url='https://github.com/amarlearning/Github-Sectory',
	author='Amar Prakash Pandey (@amarlearning)',
    long_description_content_type='text/markdown',
	long_description=long_description,
	author_email='amar.om1994@gmail.com',
	license='MIT',
	keywords='github repository download sub-directory',
	install_requires=['clint'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.7'
	],
	scripts=['github-sectory']
)
