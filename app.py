import os
import time

from config.config_manager import ConfigManager
from device.sensor_medal import SensorMedal, get_medal_data
from iot_client.cloud_iot_core import CloudIoTCoreClient

iot_core_client = None

def inject_config():
    config_manager = ConfigManager(os.path.dirname(os.path.abspath(__file__)))
    iot_core_client = CloudIoTCoreClient(config_manager)


def check_status(sensor_medal:SensorMedal):
    if sensor_medal.rssi > -55 and sensor_medal.lumix < 10:
        return 'storage'

    return 'using'


if __name__ == '__main__':

    while True:

        time.sleep(5)
        medals = get_medal_data(['ROHMMedal2_0073_01.00'])
        for medal in medals:
            print(medal)
            print(check_status(medal))