#!/usr/local/bin/python3

import time
import board
import busio
import sys
import adafruit_mcp9808
import json
import requests

# Config items
TWX_SERVER = "localhost"
TWX_THINGNAME = "ExampleThing"
TWX_APPKEY = ""

try:
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    mcp = adafruit_mcp9808.MCP9808(i2c_bus)
except IOError:
    sys.exit("Problem trying to find the sensor")

# Setup the Rest API connection properties
api_endpoint = 'https://' + TWX_SERVER + '/Thingworx/Things/' + TWX_THINGNAME + '/Properties/temperature'
api_headers= { 'Content-Type': 'application/json', 'appKey': TWX_APPKEY }

while True:
    tempC = mcp.temperature

    tempF = tempC * 9 / 5 + 32
    print('Temperature: {} C {} F '.format(tempC, tempF))

    payload = {'temperature': tempC }

    # in a production environment, the SSL certificate should be verified -- there will be warnings about this on the logger
    response = requests.put(api_endpoint, headers=api_headers, json=payload, verify=False)

    # if there's a problem, this will print out the error and quit
    response.raise_for_status()

    time.sleep(10)