# RasPyDHT
Temperature and humidity monitoring system based on RaspberryPi board.

## Key future

* Support for DHT 11/22/AM2302
* Temperature and Humidity displayed on a LCD1602
* Possibility to publish data with MQTT
* Both console application and simple GUI that plots temperature and humidity over time

## Dependency

* Adafruit Python DHT library to read data from DHT Sensor
* Sunfounder SensorKit for RPi2 library to control LCD162

## Compatibility

* Requires python 3 (3.5.3+). Earlier version of Python not tested


## How to use

The module can be used in two ways:
## Installing module
To install run `pip install dht` or checkout module and run `pip install .` from repository root folder

This installs into python allowing the app to executed from any path by simply typing `robotdataclient`

### Developer mode
If you want to be able to modify the code but still use from any location you can install it in developer mode by running `pip install -e ,`

This will install it but point to the files of this repository

## Running locally
If you do not want to install, you can also run the scripts from repository root. Like so:
$ python runme.py IP 1k|rt


## Dependencies
This module is tested with Python2.7 and Python3.5+
