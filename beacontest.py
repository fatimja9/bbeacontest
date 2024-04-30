
import time
import bluetooth._bluetooth as bluez
from beacontools import BeaconScanner, IBeaconFilter, IBeaconAdvertisement

uuid = "266B319B-5508-4267-A1B7-678B12E2F02A"
out_of_range_duration = 10
last_seen_rssi = {}
last_seen_time = 0

def callback(bt_addr, rssi, packet, additional_info):
    if packet.uuid == uuid:
        global last_seen_time
        last_seen_time = time.time()
        last_seen_rssi[bt_addr] = rssi
        print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

scanner = BeaconScanner(callback, 
                        device_filter=IBeaconFilter(uuid=uuid))
scanner.start()

try:
    while True:
        # Sleep for a short duration before checking again
        time.sleep(2)
        current_time = time.time()
        absence_duration = current_time - last_seen_time
        # for loop?
        if absence_duration > out_of_range_duration :
            print(f"Device with address {last_seen_rssi} is out of range.")
            print(f"Device was absent for", absence_duration, "seconds.")


finally:
    scanner.stop()
