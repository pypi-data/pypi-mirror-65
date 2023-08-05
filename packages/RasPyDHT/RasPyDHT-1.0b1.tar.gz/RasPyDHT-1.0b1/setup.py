from setuptools import find_packages, setup

setup(
	name='RasPyDHT',
	version='1.0-b1',
	author='William Ledda',
	author_email='villy80@hotmail.it',
	description='Temperature and humidity monitor with RaspberryPi',
	long_description='Monitoring of temperature and humidity with a DHT connected to a RaspberryPi board',
	url='https://github.com/williamledda/RasPyDHT',
	packages=find_packages(),
	install_requires=[
		'Adafruit-DHT', 
		'paho-mqtt',
		'smbus',
		],
	classifiers=[
		'Programming Language :: Python :: 3',
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
	],
)
