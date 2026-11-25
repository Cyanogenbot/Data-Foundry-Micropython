import os
import time
import network
import neopixel
import  as DF
import WifiTools as WT
from machine import Pin

led = neopixel.NeoPixel(Pin(21), 1)
wifimode = network.WLAN(network.WLAN.IF_STA)

WT.connectWifi(secrets.wifi, led, wifimode)
time.sleep(1)
gc.collect()

if wifi.isconnected():
    # Create a DF connection
    DataFoundry = DF.DataFoundry(secrets.df_url, secrets.device_id)

---

    # Setup a simple LLM
    llm = DataFoundry.AIFoundry(secrets.aitoken)

    # Send query
    query1 = llm.text(f"Create a haiku.")

    # Print response
    print("*** llm: ", response)

---

    # Setup a simple llm + model
    open_llm = DataFoundry.AIFoundry(secrets.aitoken, model="apertus-8b-instruct-2509")

    # Send query
    query2 = spicy_llm.text(f"Create a haiku.")

    # Print response
    print("*** spicy llm: ", response2)

---

    # Setup a simple LLM with temperature controls
    spicy_llm = DataFoundry.AIFoundry(secrets.aitoken, temperature = 2)

    # Send query
    query3 = open_llm.text(f"Create a haiku.")

    # Print response
    print("*** spicy llm: ", response3)
