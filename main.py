# https://wiki.dfrobot.com/Gravity:%20Analog%20SHT30%20Temp.%20%26%20RH%20Sensor_SKU_DFR0588#Example%20Codes

from machine import ADC, Pin
import time

VREF = 3.3
ADC_RES = 65535
adc_temp = ADC(Pin(27))
adc_hum = ADC(Pin(26))

while True:
    raw_temp = adc_temp.read_u16()
    raw_hum = adc_hum.read_u16()

    volt_temp = (raw_temp / ADC_RES) * VREF
    volt_hum = (raw_hum / ADC_RES) * VREF

    Tc = -66.875 + 72.917 * volt_temp

    RH = -12.5 + 41.667 * volt_hum

    print(f"Temperature: {Tc:.1f} °C")
    print(f"Humidity: {RH:.1f} %RH\n")

    time.sleep(2)
