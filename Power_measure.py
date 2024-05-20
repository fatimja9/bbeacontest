import busio
import time
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# I2C Bus erzeugen
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x48) # default Adresse 48

#                                                 ADS1015  ADS1115
#                                                 -------  -------
# ads.gain = 2/3  # 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
# ads.gain = 1    # 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
# ads.gain = 2    # 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
# ads.gain = 4    # 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
# ads.gain = 8    # 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
# ads.gain = 16   # 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV
# https://cdn-learn.adafruit.com/downloads/pdf/adafruit-4-channel-adc-breakouts.pdf
ads.gain = 1 # Gain muss passend zur messenden Spannung gesetzt werden


# Spannungsmessung als differentielle Messung 
# Shunt mit Channel 0 und 1 verbunden
#voltage_channel = AnalogIn(ads, ADS.P0, ADS.P1)
voltage_channel = AnalogIn(ads, ADS.P0)

print(f"Aktueller AD-Wert {voltage_channel.value} -  Spannung: {abs(voltage_channel.voltage)}")

sample_count = 100      # Samples
power_sum = 0
work_sum = 0

# 5V Versorgungspannung, über Shunt dürfen max. 205mV abfallen, um Raspi Pi Zero sicher zu betreiben (min, 4,75V)
# Boot-Current Raspi Pi Zeor: 250 mA: https://forums.raspberrypi.com/viewtopic.php?t=277944
# R(shunt) = Voltage-Drop / max Current
max_Current = 0.25   # 250 mA
max_Voltage = 0.25   # 250 mV
shunt_resistor = max_Voltage/max_Current    # 1 Ohm

start = time.time()
while True:
  # Messung des Stroms über die definierte Anzahl von Samples
  for _ in range(sample_count):
#    voltage_channel = AnalogIn(ads, ADS.P0, ADS.P1)
    voltage_channel = AnalogIn(ads, ADS.P0)
    voltage = abs(voltage_channel.voltage)
    current = voltage / shunt_resistor   # I = U / R
#   Leistung berechnen P = UI
    power = voltage * current
    # Aufsummierung der Leistungswerte
    power_sum += power


# Zeit berechnen 
  actual_time = time.time()
  time_difference = actual_time - start
  start = actual_time
 
  print(f"Letzte Spannung: {voltage:.4f} V")
  print(f"Letzte Stromstärke: {current:.4f} A")
  print(f"Letzte Leistung: {power:.4f} W")
 
  print(f"Zeitdauer fuer {sample_count} messungen: {time_difference}")

# Berechnung der verbrauchten Energie
  work = (power_sum/sample_count)*time_difference
  print(f"Energieverbrauch (momentan): {work:.4f} Ws")

  power_sum = 0 # Reset 

# Aufsummieren der Energie
  work_sum += work
  print(f"Gesamter Energieverbrauch: {work_sum:.4f} Ws\n")

  
  #time.sleep(1)  # Adjust as needed





