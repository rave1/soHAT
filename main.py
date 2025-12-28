# https://wiki.dfrobot.com/Gravity:%20Analog%20SHT30%20Temp.%20%26%20RH%20Sensor_SKU_DFR0588#Example%20Codes

from machine import ADC, Pin
from time import sleep
import network
import rp2
import sys
from config import SSID, PASSWORD
import requests
import json

VREF = 3.3
ADC_RES = 65535
adc_temp = ADC(Pin(27))
adc_hum = ADC(Pin(26))
led_pin = Pin("LED", Pin.OUT)


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        retry = 0
        while not wlan.isconnected():
            sleep(1)
            retry += 1
            print("Waiting for connection...", retry)
            if rp2.bootsel_button() == 1:
                print("Aborting connection.")
                sys.exit()
            if retry > 20:  # po 20 sek. spróbuj ponownie od zera
                wlan.disconnect()
                wlan.connect(SSID, PASSWORD)
                retry = 0
    print("Connected on:", wlan.ifconfig()[0])
    for i in range(6):
        led_pin.value(not led_pin.value())
        sleep(0.1)
    return wlan


wlan = connect_to_wifi()

headers = {"Content-Type": "application/json"}

while True:
    if not wlan.isconnected():
        print("Wi-Fi lost, reconnecting...")
        wlan = connect_to_wifi()

    raw_temp = adc_temp.read_u16()
    raw_hum = adc_hum.read_u16()

    volt_temp = (raw_temp / ADC_RES) * VREF
    volt_hum = (raw_hum / ADC_RES) * VREF

    Tc = -66.875 + 72.917 * volt_temp
    RH = -12.5 + 41.667 * volt_hum

    payload = {"temp": Tc, "humidity": RH}
    url = "http://192.168.123:8000/temp"
    try:
        r = requests.post(
            url, data=json.dumps(payload), headers=headers
        )
        print("Sent JSON:", payload, "→", r.status_code)
        r.close()
    except Exception as e:
        print("Request failed:", e)
    sleep(2)
