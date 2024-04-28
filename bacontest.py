import bluetooth._bluetooth as bluez
import struct
import time
from beacontools import BeaconScanner, IBeaconFilter

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

# scan for all iBeacon advertisements from beacons with the specified uuid 
scanner = BeaconScanner(callback, 
    device_filter=IBeaconFilter(uuid="e5b9e3a6-27e2-4c36-a257-7698da5fc140")
)
scanner.start()
time.sleep(5)
scanner.stop()

# scan for all iBeacon advertisements regardless from which beacon
scanner = BeaconScanner(callback,
    packet_filter=IBeaconAdvertisement
)

# parse
tlm_packet = b"\x02\x01\x06\x03\x03\xaa\xfe\x11\x16\xaa\xfe\x20\x00\x0b\x18\x13\x00\x00\x00" \
             b"\x14\x67\x00\x00\x2a\xc4\xe4"
tlm_frame = parse_packet(tlm_packet)
print("Voltage: %d mV" % tlm_frame.voltage)
print("Temperature: %d °C" % tlm_frame.temperature)
print("Advertising count: %d" % tlm_frame.advertising_count)
print("Seconds since boot: %d" % tlm_frame.seconds_since_boot)

scanner.start()


def check_in_range():
    global detected_devices
    
    current_time = time.time()
    devices_back_in_range = {}
    
    # Iteriere über die erkannten Geräte
    for device, last_seen_time in detected_devices.items():

        # Wenn das Gerät länger als 5 Sekunden nicht gesehen wurde, gilt es als wieder in Reichweite
        if current_time - last_seen_time > 5:
            devices_back_in_range[device] = current_time - last_seen_time
    
    return devices_back_in_range

scanner = BeaconScanner(callback, 
    device_filter=IBeaconFilter(uuid="e5b9e3a6-27e2-4c36-a257-7698da5fc140") )

scanner.start()

 while True:
        # warte 5 Sekunden
        time.sleep(5)
        
        # ob Geräte wieder in Reichweite sind und melde die Zeit der Abwesenheit
        devices_in_range = check_in_range()
        
        if devices_in_range:
            for device, absence_time in devices_in_range.items():
                print("Device", device, "was absent for", absence_time, "seconds.")

 scanner.stop()
