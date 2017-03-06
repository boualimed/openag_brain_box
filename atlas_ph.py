"""
Code for interfacing with Atlas Scientific pH sensor connected to usb adaptor board
"""
from atlas_device import AtlasDevice

class AtlasPh:
    """
    Class that represents an Atlas Scientific pH sensor instance and provides functions
    for interfacing with the sensor.
    """

    def __init__(self, device_id, pseudo=False):
        self.device_id = device_id # TODO: auto detect ids, i wonder if atlas
        # circuit ids have a consistent pattern to differentiate between ph & ec
        self.pseudo = pseudo
        self.sensor_is_connected = True
        self.ph = None
        self.connect()

    def connect(self):
        if not self.pseudo:
            try:
                self.device = AtlasDevice(self.device_id)
                self.device.send_cmd('C,0') # turn off continuous mode
                time.sleep(1)
                dev.flush()
                print('Connected to Atlas pH sensor')
            except:
                if self.sensor_is_connected:
                    print('Unable to connect to Atlas pH sensor')
                    self.sensor_is_connected = False
        else:
            print('Connected to pseudo Atlas pH sensor')

    def poll(self):
        if not self.pseudo:
            try:
                self.device.send_cmd("R")
                lines = self.device.read_lines()
                for i in range(len(lines)):
                    if lines[i] != u'*OK\r':
                        self.ph = float(lines[i])
            except:
                self.ph = None
                self.connect()
        else:
            self.ph = 6.4

    def transmitToConsole(self):
        if self.ph is not None:
            print('AtlasPh pH: ', self.ph, 'pH')

    def transmitToMemcache(self, memcache_shared, ph_id='ph'):
        if self.ph is not None:
            memcache_shared.set(id, "{0:.1f}".format(self.ph))