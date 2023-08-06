#!/usr/bin/env python3
from . import LCD1602
import time
import datetime as dt
import threading


class DHTLcd(threading.Thread):
    def __init__(self, name=''):
        super().__init__(name=name)

    def setup(self):
        LCD1602.init(0x27, 1)  # init(slave address, background light)
        LCD1602.write(0, 0, 'Welcome MyDHTPi!')
        LCD1602.write(1, 1, 'Room ' + self.name)
        time.sleep(2)

    def run(self):
        self.setup()
        now = dt.datetime.now()
        # Wait till next full second
        time.sleep((1e6 - now.microsecond) / 1e6)

        while not getattr(threading.currentThread(), "stop", False):
            now = dt.datetime.now()
            humidity = getattr(threading.currentThread(), "humidity", None)
            temperature = getattr(threading.currentThread(), "temperature", None)

            if humidity is not None and temperature is not None:
                line = '{0:0.1f} (C) - {1:3.0f} %'.format(temperature, humidity)
            else:
                line = 'XX.Y (C) - HHH %'

            LCD1602.write(0, 0, now.strftime('%d/%m - %H:%M:%S'))
            LCD1602.write(0, 1, line)

            # Wait till next full second
            time.sleep((1e6 - now.microsecond) / 1e6)

        LCD1602.clear()
        LCD1602.write(0, 0, "Sopping...")
        LCD1602.write(0, 1, "Bye Bye!!")
        time.sleep(2.0)

    def destroy(self):
        LCD1602.clear()
        pass


if __name__ == "__main__":
    lcd = DHTLcd(name='Test')
    try:
        lcd.start()
        while True:
            pass
    except KeyboardInterrupt:
        lcd.stop = True
        lcd.join()
        lcd.destroy()
