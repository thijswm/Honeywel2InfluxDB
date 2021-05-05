#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()
import os
import json

""" Lyric API Settings """
LYRIC_CLIENT_ID = os.environ['LYRIC_CLIENT_ID']
LYRIC_CLIENT_SECRET = os.environ['LYRIC_CLIENT_SECRET']
LYRIC_APP_NAME = os.environ['LYRIC_APP_NAME']
LYRIC_REDIRECT_UI = os.environ['LYRIC_REDIRECT_UI']
LYRIC_TOKEN = json.loads(os.environ['LYRIC_TOKEN'])

""" Influx Settings """
INFLUX_URL = os.environ['INFLUX_URL']
INFLUX_DB = os.environ['INFLUX_DB']
INFLUX_USERNAME = os.environ.get('INFLUX_USERNAME','')
INFLUX_PASSWORD = os.environ.get('INFLUX_PASSWORD','')

POLL_INTERVAL = int(os.environ.get('POLL_INTERVAL', 120))
DEBUG_MODE = bool(os.environ.get('DEBUG_MODE', False))

from time import sleep
from lyric import Lyric
from influxdb_client import InfluxDBClient,Point
import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger()
if DEBUG_MODE:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

def loop():
    lapi = Lyric(
      client_id = LYRIC_CLIENT_ID,
      client_secret = LYRIC_CLIENT_SECRET,
      token = LYRIC_TOKEN,
      redirect_uri = LYRIC_REDIRECT_UI,
      app_name = LYRIC_APP_NAME)

    token = ""
    if INFLUX_USERNAME and INFLUX_PASSWORD:
        token = "{}:{}".format(INFLUX_USERNAME,INFLUX_PASSWORD)

    logger.info(f"Influx url:{INFLUX_URL}")
    
    bucket = INFLUX_DB
    with InfluxDBClient(url=INFLUX_URL,token=token,org='-') as client:
        with client.write_api() as write_api:
            while(True):
              for location in lapi.locations:  
                for thermostat in location.thermostats:
                    uniqueId = "{}:{}".format(location.name,thermostat.name)
                    indoorTemperature = float(thermostat.indoorTemperature)
                    temperatureSetPoint = float(thermostat.temperatureSetpoint)  
                    point = Point(uniqueId).field("indoorTemperature",indoorTemperature).field("temperatureSetPoint",temperatureSetPoint)                    
                    write_api.write(bucket=bucket,record=point)
              sleep(POLL_INTERVAL)

if __name__ == '__main__':
    logger.info("Starting")
    try:
        loop()
    except KeyboardInterrupt:        
        logger.info("Stop")