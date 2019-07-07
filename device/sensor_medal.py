import time

from bluepy import btle
import struct


class SensorMedal:

    def __init__(self, deviceID, rssi, sensor_data):
        self.deviceId = deviceID
        self.rssi = rssi
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0
        self.pressure = 0
        self.lumix = 0
        self._parse_sensor_data(sensor_data)

    def _parse_sensor_data(self, sensor_data):
        self.accel_x = struct.unpack('<h', sensor_data[8:10])[0] / 4096
        self.accel_y = struct.unpack('<h', sensor_data[10:12])[0] / 4096
        self.accel_z = struct.unpack('<h', sensor_data[12:14])[0] / 4096
        self.pressure = struct.unpack('<i', sensor_data[20:23]+b'\x00')[0] / 2048
        self.lumix = struct.unpack('<h', sensor_data[23:25])[0] / 1.2

    def __str__(self):
        ret = "SensorMedal: deviceId:{DEVICE_ID} rssi:{RSSI}" \
              " x:{ACCEL_X} y:{ACCEL_Y} z:{ACCEL_Z}" \
              " pressure:{PRESS} lumix:{LUX}"\
            .format(DEVICE_ID=self.deviceId, RSSI=self.rssi,
                    ACCEL_X=self.accel_x, ACCEL_Y=self.accel_y, ACCEL_Z=self.accel_z,
                    PRESS=self.pressure, LUX=self.lumix)
        return ret



class MedalManager:

    def check_status(self, sensor_medal:SensorMedal):
        if sensor_medal.rssi > -55 and sensor_medal.lumix < 10:
            return 'storage'

        return 'using'

    def get_medal_data(self, device_ids):

        scanner = btle.Scanner(0)
        devices = scanner.scan(3.0)
        sensor_medals = []
        for d in devices:
            try:
                if d.scanData[8].decode() in device_ids:
                    sensor_medal = SensorMedal(d.scanData[8], d.rssi, d.scanData[255])
                    sensor_medals.append(sensor_medal)
            except KeyError:
                pass

        return sensor_medals



