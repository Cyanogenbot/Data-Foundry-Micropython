# WifiTools.py
# A MicroPython to make working with Wifi easier
# Written by Diede van Marle

import os
import time
import network
import neopixel
import
from machine import Pin
# WifiTools.py
import time

def connectWifi(wifi_dict, led, wifi):
    """
    Connect to WiFi network
    Returns: True if connected, False if failed
    """
    # Wifi Connection function
    led.fill((0, 20, 0))  # Indicate trying to connect
    led.write()

    try:
        # Reset WiFi module to clear any previous errors
        wifi.active(False)
        time.sleep(0.5)  # Give it time to fully deactivate
        wifi.active(True)
        time.sleep(0.5)  # Give it time to fully activate
    except Exception as e:
        print(f"*** WIFI: Error activating WiFi module: {e}")
        led.fill((20, 0, 0))
        led.write()
        return False

    if wifi.isconnected():
        print("*** WIFI: Already connected")
        print(f"*** WIFI: IP address: {wifi.ifconfig()[0]}")
        led.fill((0, 0, 20))
        led.write()
        return True

    print('*** WIFI: Connecting to network...')

    # Try each network in the dictionary
    for ssid in wifi_dict:
        wifipassword = wifi_dict[ssid]
        print(f"*** WIFI: Trying to connect to {ssid}...")

        try:
            # Ensure we're disconnected before attempting new connection
            try:
                wifi.disconnect()
                time.sleep(0.5)
            except:
                pass

            wifi.connect(ssid, wifipassword)
            timeout = 10  # Timeout after 10 seconds
            start_time = time.time()

            # Check if the Wi-Fi is connected within the timeout period
            while not wifi.isconnected():
                current_status = wifi.status()

                # Check for specific error codes
                if current_status == -202:  # Connection failed
                    print(f"*** WIFI: Connection to {ssid} failed (error -202)")
                    break
                elif current_status < 0:  # Any negative status is an error
                    print(f"*** WIFI: Connection error: {current_status}")
                    break

                if time.time() - start_time > timeout:
                    print(f"*** WIFI: Timeout connecting to {ssid}")
                    break

                time.sleep(0.1)

            # Check if successfully connected
            if wifi.isconnected():
                print(f"*** WIFI: Connected to {ssid}")
                print(f"*** WIFI: IP address: {wifi.ifconfig()[0]}")
                return True
            else:
                # Force disconnect after failed attempt
                try:
                    wifi.active(False)
                    time.sleep(0.3)
                    wifi.active(True)
                    time.sleep(0.3)
                except:
                    pass


        except Exception as e:
            print(f"*** WIFI: Error connecting to {ssid}: {e}")
            try:
                wifi.active(False)
                time.sleep(0.3)
                wifi.active(True)
                time.sleep(0.3)
            except:
                pass
            continue

    # Final status - failed to connect to any network
    print("*** WIFI: Couldn't connect to any network")
    return False
