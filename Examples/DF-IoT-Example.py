import os
import time
import network
import neopixel
import json
import random
import  as DF
import WifiTools as WT
from machine import Pin

led = neopixel.NeoPixel(Pin(21), 1)
wifimode = network.WLAN(network.WLAN.IF_STA)

WT.connectWifi(secrets.wifi, led, wifimode)
time.sleep(1)
gc.collect()

if wifi.isconnected():
    DataFoundry = DF.DataFoundry(secrets.df_url, secrets.device_id)
    dataset = DataFoundry.IoTDataset(secrets.dataset_id, secrets.dataset_token)

    datasend = {'temperature':random.randint(0,254), "door":random.choice(["Open","Closed"])}
    dataset.send(datasend)
