import busio
import time
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# I2C Bus erzeugen
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x48) # default Adresse 48
ads.gain = 1

# AnalogIn-Objekts für differenzielle Messung
chan = AnalogIn(ads, ADS.P0, ADS.P1)

# Spannungsmessung
voltage_channel = AnalogIn(ads, ADS.P2)
voltage = voltage_channel.voltage

sample_count = 860  
current_sum = 0
shunt_resistor_ohms = 0.1 

while True:
  print(f"Spannung: {voltage:.4f} V")
  
  # Messung des Stroms über die definierte Anzahl von Samples
  for _ in range(sample_count):
    voltage = chan.voltage
    current = voltage / shunt_resistor_value    # I = U / R
    # Aufsummierung der Stromwerte
    current_sum += current
    time.sleep(1e-3) 

  # Leistung berechnen und Ausgabe P = UI
  power = voltage * current_sum
  print(f"Leistung: {power:.4f} W")
  time.sleep(1)  # Adjust as needed
