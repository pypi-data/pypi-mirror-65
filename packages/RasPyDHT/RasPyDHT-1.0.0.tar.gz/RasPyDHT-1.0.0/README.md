# RasPyDHT
Temperature and humidity monitoring system based on RaspberryPi board.

## Key future

* Support for DHT 11/22/AM2302.
* Temperature and Humidity displayed on a LCD1602.
* Possibility to publish data with MQTT.
* Both console application and simple GUI that plots temperature and humidity over time.

## Dependency

* Requires python 3 (3.5.3+). It should work also on earlier version of Python 3, but not tested.
* Adafruit Python DHT library to read data from DHT Sensor (https://github.com/adafruit/Adafruit_Python_DHT).
* Sunfounder SensorKit for RPi2 library to control LCD162 (https://github.com/sunfounder/SunFounder_SensorKit_for_RPi2).
* smbus.
* matplotlib.

## How to use

There are many ways you can use this package:

* Checkout this repository and run the script locally (see later).
* Installing the module.

## Installing module
To install, run `pip install raspydht` or checkout this repository and run `pip install .` from repository root folder
This installs into python allowing the scripts to executed from any path.

You can also install on a virtual environment (e.g. virtualenv) for testing it.

### Developer mode
If you want to be able to modify the code but still use from any location, you can checkout this repositorya amd 
install it in developer mode by running `pip install -e .`. 
This will install it but point to the files of this repository.

### Running locally
If you do not want to install, you can also checkout the repository and run the scripts from repository root. 
In this case you need to install the dependencies manually 

## Scripts
Thi package contains two applications that can be run as scripts

* ``rasdpydht``: is a console application that read data from the DHT sensor and display temperature and humidity 
on a LCD1602. Optionally it can also publish these data with MQTT protocol.
* ``raspydhtplot``: simple GUI application that plot temperature and DHT over time.

### raspydht

By installing the application (either with pip or from the local repository) you can run this application from any path
by simply typing ``raspydht``

If you have instead decide to do not install you can always run the application from the local repository as follow:

```bash
$ cd <local repository root>
$ python3 -m raspydht 
```

or 

```bash
$ cd <local repository root>
$ python3 runconsole.py  
```

Whatever option you choose, the following command line options are available:

```bash 
  -h, --help       show this help message and exit
  --type TYPE      dht sensor type (11, 22, or 2302, default 22)
  --gpio GPIO      GPIO port number (default is 4)
  --sleep SLEEP    Delay (s) between two readings (default 2)
  --broker BROKER  MQTT broker host (default None)
  --verbose        Log info into console (default false)
  --room ROOM      Room name (default )
```

### raspydhtplot

By installing the application (either with pip or from the local repository) you can run this application from any path
by simply typing ``raspydhtplot``. Differently from the console application, it doesn't support MQTT protocol. 

If you have instead decide to do not install you can always run the application from the local repository as follow:

```bash
$ cd <local repository root>
$ python3 -m raspydhtplot 
```

or 

```bash
$ cd <local repository root>
$ python3 runplot.py  
```

Whatever option you choose, the following command line options are available:

```bash 
  -h, --help     show this help message and exit
  --type TYPE    dht sensor type (11, 22, or 2302, default 22)
  --gpio GPIO    GPIO port number, default 4
  --sleep SLEEP  Delay (s) between two readings, default 2
  --verbose      Log info into console
```