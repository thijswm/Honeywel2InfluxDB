#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()
import os

""" Honeywell API Settings """
LYRIC_CLIENT_ID = os.environ['LYRIC_CLIENT_ID']
LYRIC_CLIENT_SECRET = os.environ['LYRIC_CLIENT_SECRET']
LYRIC_APP_NAME = os.environ['LYRIC_APP_NAME']
LYRIC_REDIRECT_UI = os.environ['LYRIC_REDIRECT_UI']
LYRIC_TOKEN = os.environ['LYRIC_TOKEN']

""" Influx Settings """
INFLUX_HOST     = os.environ['INFLUX_HOST']
INFLUX_DB       = os.environ['INFLUX_DB']
""" Optional Influx Settings """
INFLUX_PORT     = os.environ.get('INFLUX_PORT', 8086)
INFLUX_USERNAME = os.environ.get('INFLUX_USERNAME',None)
INFLUX_PASSWORD = os.environ.get('INFLUX_PASSWORD',None)

POLL_INTERVAL = os.environ.get('POLL_INTERVAL', 120)

DEBUG_MODE = os.environ.get('DEBUG_MODE', False)

from time import sleep
from lyric import Lyric
from influxdb import InfluxDBClient
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger()
if DEBUG_MODE:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def loop():
    lapi = Lyric(
      client_id = client_id,
      client_secret = client_secret,
      token_cache_file = token_cache_file,
      redirect_uri = redirect_uri,
      app_name = app_name)

    influxClient = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT,username=INFLUX_USERNAME,password=INFLUX_PASSWORD)
    influxClient.switch_database(INFLUX_DB)
    
    while(True):
      for location in lapi.locations:  
        for thermostat in location.thermostats:
            uniqueId = "{}:{}".format(location.name,thermostat.name)
            indoorTemperature = float(thermostat.indoorTemperature)
            heatSetPoint = float(thermostat.heatSetpoint)  
            influxBody = [{"measurement":uniqueId,"fields":{"indoorTemperature":indoorTemperature,"heatSetpoint":heatSetPoint}}]
            influxClient.write_points(influxBody)
      sleep(POLL_INTERVAL)
    

if __name__ == '__main__':
    logger.info("Start")
    try:
        loop()
    except KeyboardInterrupt:        
        logger.info("Stop")