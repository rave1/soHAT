# https://wiki.dfrobot.com/Gravity:%20Analog%20SHT30%20Temp.%20%26%20RH%20Sensor_SKU_DFR0588#Example%20Codes

from machine import ADC, Pin
from time import sleep
import network
import rp2
import sys
from config import SSID, PASSWORD
import requests

VREF = 3.3
ADC_RES = 65535
adc_temp = ADC(Pin(27))
adc_hum = ADC(Pin(26))


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        if rp2.bootsel_button() == 1:
            sys.exit()
        print("Waiting for connection...")
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


connect_to_wifi()

while True:
    raw_temp = adc_temp.read_u16()
    raw_hum = adc_hum.read_u16()

    volt_temp = (raw_temp / ADC_RES) * VREF
    volt_hum = (raw_hum / ADC_RES) * VREF

    Tc = -66.875 + 72.917 * volt_temp

    RH = -12.5 + 41.667 * volt_hum

    requests.post(url="http://192.168.123/temp", data={"temp": Tc, "humidity": RH})

    sleep(2)
