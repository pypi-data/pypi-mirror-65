from setuptools import setup

with open('README.txt', encoding='UTF-8') as f:
	a=f.read()

setup(
	name='daad2msxcas',
	author="Pedro Fernández",
	author_email="rockersuke@gmail.com",
	version='1.0b2',
	license="MIT",	
	url="https://www.zonafi.es",
	description="Crea ficheros cas de MSX para aventuras hechas con el DAAD.",
	long_description=a,
	python_requires=">=3.8",
	scripts=['daad2msxcas.py']
)