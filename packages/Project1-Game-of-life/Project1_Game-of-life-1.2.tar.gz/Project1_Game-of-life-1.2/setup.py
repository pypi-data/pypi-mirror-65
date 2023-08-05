# setup.py
from setuptools import setup

setup(name='Project1_Game-of-life',
	version='1.2',
	description='Project for the course "Advanced Scientific Programming in Python", 23-27 March 2020, Uppsala University.',
	url='https://github.com/rafael-mrden/Project1_Game-of-life',
	author='Rafael Mrden',
	author_email='rafael.mrdjen@gmail.com',
	license='BSD',
	py_modules=['gameoflife'],
	install_requires=['numpy', 'matplotlib'],
	packages=[])
