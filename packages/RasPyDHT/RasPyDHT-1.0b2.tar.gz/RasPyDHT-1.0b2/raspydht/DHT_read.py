#!/usr/bin/python

import sys
import time
import argparse
import Adafruit_DHT
import paho.mqtt.client as mqtt
from .DHT_lcd1602 import DHTLcd


# Parse command line parameters.
def parse_cmd_option():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='22', help='dht sensor type (11, 22, or 2302)')
    parser.add_argument('--gpio', type=int, default=4, help='GPIO port number')
    parser.add_argument('--sleep', type=int, default=2, help='Delay (s) between two readings')
    parser.add_argument('--broker', default=None, help='MQTT broker host')
    parser.add_argument('--verbose', action="store_true", help='Log info into console')
    parser.add_argument('--room', default='Room_1', help='Room name')
    return parser.parse_args()


def publish_data(mqtt_client, temp, hum, client_id):
    if mqtt_client.is_connected():
        mqtt_client.publish('RasPyDHT/' + client_id + '/temperature', temp)
        mqtt_client.publish('RasPyDHT/' + client_id + '/humidity', hum)


def on_connect_cbk(client, userdata, flags, rc):
    if rc == 0:
        print("Client connected: " + str(client.is_connected()))
    else:
        print("Error connecting to broker: " + str(rc))


def on_disconnect_cbk(client, flags, rc):
    if rc == 0:
        print("Client disconnected")
    else:
        print("Error when disconnecting from broker: " + str(rc))


def mqtt_init(args, client):
    client.on_connect = on_connect_cbk
    client.on_disconnect = on_disconnect_cbk

    # Connect and start network loop in case a MQTT broker is provided
    if args.broker is not None:
        try:
            if args.verbose:
                print('Connecting to broker: ' + args.broker)
            client.connect(args.broker)
            client.loop_start()  # Start mqtt network loop
        except ConnectionRefusedError:
            print('Connection refused to broker: ' + args.broker)


def mqtt_stop(args, client):
    if client.is_connected():
        if args.verbose:
            print('Disconnecting client')
        client.disconnect()

    if args.broker is not None:
        client.loop_stop()


if __name__ == "__main__":
    sensor_type = {'11': Adafruit_DHT.DHT11,
                   '22': Adafruit_DHT.DHT22,
                   '2302': Adafruit_DHT.AM2302}
    args = parse_cmd_option()
    dht = sensor_type[args.type]

    client_id = args.room.replace(' ', '_')
    client = mqtt.Client(client_id)

    # Create thread for handling LCD
    lcd = DHTLcd(name=args.room)

    try:
        lcd.start()

        mqtt_init(args, client)

        while True:
            humidity, temperature = Adafruit_DHT.read_retry(dht, args.gpio)

            if humidity is not None and temperature is not None:
                if client.is_connected():
                    publish_data(client, temperature, humidity, client_id)

                lcd.humidity = humidity
                lcd.temperature = temperature

                if args.verbose:
                    print('{0:0.1f},{1:0.1f}'.format(temperature, humidity))

            sys.stdout.flush()
            time.sleep(args.sleep)

    except KeyboardInterrupt:
        lcd.stop = True
        lcd.join()
        lcd.destroy()

        mqtt_stop(args, client)

        sys.stdout.write("\rComplete!            \n")
        sys.exit(1)
