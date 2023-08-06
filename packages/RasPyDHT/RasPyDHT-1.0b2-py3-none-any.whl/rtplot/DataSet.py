import datetime as dt


class DataSet:
    def __init__(self):
        self.x = []
        self.y = []
        self.lpf = 0
        self.__ALPHA__ = 1 / 5  # alpha exponent
        self.__DUMP__ = 1 - self.__ALPHA__

    def append(self, time, measure):
        self.x.append(time)

        if (len(self.y) == 0):
            self.lpf = measure
        else:
            # Low pass filter of measured valued. Approximate moving average with exponential smoothing function
            self.lpf = (self.__ALPHA__ * measure) + (self.__DUMP__ * self.lpf)

        self.y.append(round(self.lpf, 1))

    def resize(self, newsize):
        self.x = self.x[-newsize:]
        self.y = self.y[-newsize:]
