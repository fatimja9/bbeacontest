
import struct
import time
import bluetooth._bluetooth as bluez
from beacontools import BeaconScanner, IBeaconFilter, IBeaconAdvertisement

uuid = "266B319B-5508-4267-A1B7-678B12E2F02A"
out_of_range_duration = 10 
last_seen_rssi = {}

def callback(bt_addr, rssi, packet, additional_info):
    if packet.uuid == uuid:
        last_seen_time = time.time()
        last_seen_rssi[bt_addr] = rssi
        print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

scanner = BeaconScanner(callback, 
                        device_filter=IBeaconFilter(uuid=uuid))
scanner.start()

try:
    while True:
        current_time = time.time()
        absence_duration = current_time - last_seen_time[bt_addr]
        # for loop?
        if absence_duration > out_of_range_duration :
            print(f"Device with address {bt_addr} is out of range.")
            print(f"Device was absent for", absence_duration, "seconds.")

        # Sleep for a short duration before checking again
        time.sleep(2)
finally:       
scanner.stop()
