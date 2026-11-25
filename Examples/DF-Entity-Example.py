# import requests library
import urequests
from machine import Pin
import time
import network

import json
import neopixel
import gc
import secrets
import DataFoundry as DF
import WifiTools as WT

# Setup wifi and led
wifimode = network.WLAN(network.WLAN.IF_STA)
led = neopixel.NeoPixel(Pin(21), 1)

# Connect to WiFi
WT.connectWifi(secrets.wifi, wifimode)
time.sleep(1)

# Clean up storage
gc.collect()

# API endpoint
if wifi.isconnected():

    # Setup Data Foundry instance & Dataset information
    DataFoundry = DF.DataFoundry(secrets.df_url, secrets.device_id)
    dataset = DataFoundry.EntityDataset(secrets.dataset_id, secrets.dataset_token)

    # Add database entry
    datasend = {'temperature':11, "door":"closed"}
    dataset.add("homeStatusTest", datasend, "mysecret")

    # Modify database entry
    datasendModified = {'temperature':12, "door":"closed"}
    dataset.put("homeStatusTest", datasendModified, "mysecret")

    # Remove entry from database
    # dataset.delete("homeStatusTest", "mysecret")

    # Retrieve entry from database
    result = dataset.get("homeStatusTest", "mysecret")

    try:
        json.loads(result)
        print("Found: ", json.loads(result))
    except:
        print("No json or data found")
