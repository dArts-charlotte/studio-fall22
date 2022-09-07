from typing import List

import adafruit_scd30
import board
import adafruit_tca9548a
from config import *


class Co2Sensor:
    def __init__(self, sensor_tsl, name):
        self.name = name
        self.sensor_tsl = adafruit_scd30.SCD30(sensor_tsl)

    def read_sensor(self):
        co2, temp, humidity = None, None, None
        if self.sensor_tsl.data_available:
            co2 = self.sensor_tsl.CO2
            temp = self.sensor_tsl.temperature
            humidity = self.sensor_tsl.relative_humidity
        return {"co2": co2, 'temperature': temp, 'humidity': humidity}


class SensorController:
    def __init__(self):
        # Create I2C bus as normal
        i2c = board.I2C()  # uses board.SCL and board.SDA
        # Create the Sensor TCA9548A object and give it the I2C bus
        tca = adafruit_tca9548a.TCA9548A(i2c)
        self.sensors = {}
        self.setup_sensors(tca)

    def setup_sensors(self, tca):
        """self.sensors = {
            AirSensorType: list of sensors with type AirSenor,
            SoilSensorType: list of sensors with type SoilSensor
            ...
        }"""

        for tsl, name in TSLs:
            self.sensors[name] = Co2Sensor(sensor_tsl=tca[tsl], name=name)

    def read_sensors(self):
        samples = {}
        for sensor in self.sensors:
            sample = sensor.read_sensor()
            samples[sensor.name] = sample

        return samples

    def publish_sensors(self):
        raise NotImplementedError


sensor_controller = SensorController()
