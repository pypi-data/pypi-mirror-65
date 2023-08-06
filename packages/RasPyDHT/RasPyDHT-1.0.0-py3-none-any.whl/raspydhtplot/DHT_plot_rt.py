#!/usr/bin/env python

# Reference
# https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time


import sys
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Adafruit_DHT
import datetime as dt
from .DataSet import DataSet

fig = plt.figure()
tPlot = fig.add_subplot(2, 1, 1)
hPlot = fig.add_subplot(2, 1, 2)
args = None
sensor_type = {'11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302}
    
    
# This function is called periodically from FuncAnimation
def plot_update(i, t, h):
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor_type[args.type], args.gpio)
    
    # Un-comment the line below to convert the temperature to Fahrenheit.
    # temperature = temperature * 9/5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        if args.verbose:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

        # Add x and y to lists
        now = dt.datetime.now().strftime('%H:%M:%S')

        #append nre data
        t.append(now, temperature)
        h.append(now, humidity)

        #Resize dataset
        t.resize(30)
        h.resize(30)

        # Draw x and y lists
        tPlot.clear()
        tPlot.plot(t.x, t.y)

        hPlot.clear()
        hPlot.plot(h.x, h.y)

        #https://stackoverflow.com/questions/19273040/rotating-axis-text-for-each-subplot
        #Roatate x-axes of each plot to show date properly
        for ax in fig.axes:
            plt.sca(ax)
            plt.xticks(rotation=45)

        #Abjust the distance between sublots
        fig.tight_layout()
    else:
        if args.verbose:
            print('Failed to get reading. Try again!')


def parse_cmd_options():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='22', help='dht sensor type (11, 22, or 2302, default 22)')
    parser.add_argument('--gpio', type=int, default=4, help='GPIO port number, default 4')
    parser.add_argument('--sleep', type=int, default=2, help='Delay (s) between two readings, default 2')
    parser.add_argument('--verbose', action="store_true", help='Log info into console')
    args = parser.parse_args()


def main():
    try:
        parse_cmd_options()
        #Create two datasets, one for tempreture and one for humidity
        temp = DataSet()
        humidity = DataSet()
        ani = animation.FuncAnimation(fig, plot_update, fargs=(temp, humidity), interval=args.sleep*1000)
        plt.show()

    except KeyboardInterrupt:
        sys.stdout.write("\rComplete!            \n")


