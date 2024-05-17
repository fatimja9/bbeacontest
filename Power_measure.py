import busio
import time
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# I2C Bus erzeugen
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x48) # default Adresse 48
ads.gain = 1

# AnalogIn-Objekts f  r differenzielle Messung
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

# Spannungsmessung
voltage_channel = AnalogIn(ads, ADS.P1)
voltage = voltage_channel.voltage

sample_count = 100      # Samples
current_sum = 0
shunt_resistor = 0.1    # Ohm

while True:
  start = time.time()
  print(f"Spannung: {voltage:.4f} V") 
  # Messung des Stroms   ber die definierte Anzahl von Samples
  for _ in range(sample_count):
    voltage_channel = AnalogIn(ads, ADS.P1)
    voltage = voltage_channel.voltage
    current = voltage / shunt_resistor   # I = U / R
    # Aufsummierung der Stromwerte
    current_sum += current
#    time.sleep(1/sample_count)
  print(f"Zeitdauer fuer {sample_count} messungen: {time.time() - start}")

  # Leistung berechnen und Ausgabe P = UI
  power = voltage * current_sum/sample_count
  print(f"Leistung: {power:.4f} W")
  #time.sleep(1)  # Adjust as needed





