import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# I2C Bus erzeugen
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x48) # default Adresse 48

# single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

while True:
  # Spannungsmessung
  voltage_channel = AnalogIn(ads, ADS.P0)
  voltage = voltage_channel.voltage

  # Anzahl der Samples für die Strommessung
  sample_count = 860
  current_sum = 0

  # Messung des Stroms über die definierte Anzahl von Samples
  # for _ in range(sample_count):
    # Messung des Stroms und Aufsummierung
    #  current_sum += current_channel.value ???????

  # Leistung berechnen und Ausgabe P = UI
  power = voltage * current_sum
  print("{:>5}\t{:>5}".format("Leistung:", power, "w"))
