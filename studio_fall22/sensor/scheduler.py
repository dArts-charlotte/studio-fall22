import logging
from apscheduler.schedulers.background import BlockingScheduler
from sensor import sensor_controller
from typing import Dict, List
from csv import DictWriter
from config import *

class SensorScheduler:

    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.status = False
        self.initiated = False

    @staticmethod
    def store_samples(samples: Dict, file_name: str):
        with open(file_name, 'a') as csv_file:
            fields = samples.keys()
            dict_writer = DictWriter(csv_file, fields)
            dict_writer.writerow(samples)
            csv_file.close()

    def sensor_read_and_publish(self):
        samples = sensor_controller.read_sensors()
        self.store_samples(samples, SAMPLE_FILE)
        print(samples)
        logging.info(samples)

    def create_sensor_job(self):
        self.scheduler.add_job(self.sensor_read_and_publish, 'interval', seconds=SENSOR_READING_INTERVALS_IN_SEC)

    def start(self):
        if not self.status:
            self.scheduler.start() if not self.initiated else self.scheduler.resume()
            self.status = True
            self.initiated = True

    def pause(self):
        if self.status:
            self.scheduler.pause()
            self.status = False


sensor_scheduler = SensorScheduler()
