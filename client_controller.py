import threading
import time
import json
from json import JSONDecodeError

from device.sensor_medal import SensorMedal, MedalManager
from iot_client.cloud_iot_core import CloudIoTCoreClient
from logging import getLogger




class ClientController:

    logger = getLogger(__name__)

    def __init__(self, mqtt_client: CloudIoTCoreClient, medal_manager: MedalManager):
        self.event = None

        self.mqtt_client = mqtt_client
        self.mqtt_client.setObserver(self)
        self.medal_manager = medal_manager
        self.deviceList = []

    def search(self):
        while True:
            time.sleep(5)
            medals = self.medal_manager.get_medal_data(['ROHMMedal2_0073_01.00'])
            for medal in medals:
                self.logger.info(medal)
                self.logger.info(self.medal_manager.check_status(medal))
                try:
                    d = {'status':self.medal_manager.check_status(medal),
                         'accel_x':medal.accel_x, 'accel_y':medal.accel_y ,'accel_z':medal.accel_z,
                         'pressure':medal.pressure, 'lumix':medal.lumix,'rssi':medal.rssi}
                    payload = json.dumps(d)
                    self.mqtt_client.publish_telemetry(payload,'object')
                except KeyError or TypeError:
                    self.logger.warning("Failed get device info {}".format(result))
                except TypeError:
                    self.logger.warning("Device info is type error. must be dict {}".format(result))
                except JSONDecodeError as e:
                    self.logger.warning("Failed device info serialized to string by json.dumps ")


    def start(self):
        search_thread = threading.Thread(target=self.search)
        search_thread.start()
        self.mqtt_client.connect()

    def notify(self, event):
        self.logger.debug("Get event from IoT Core: {}".format(event))
        event.split('')

        #event_map = json.loads(event)
        #self._event_router(event_map)

    def _event_router(self, event):

        if event['event'] == 'press':
            self.logger.info("process press event.")
            self._press_switch()
        elif event['event'] == 'turn_on':
            self.logger.info("process turn_on event.")
            self._turn_on()
        elif event['event'] == 'turn_off':
            self.logger.info("process turn_off event.")
            self._turn_off()
        elif event['event'] == 'status':
            self.logger.info("process status event")
            self._status()
        else:
            self.logger.info("Failed routing event process. :{}".format(event))

    def _press_switch(self):
        self.switchBot.press_switch()
        self.mqtt_client.publish_telemetry('event success.', 'ackevent')

    def _turn_on(self):
        self.switchBot.turn_on_switch()

    def _turn_off(self):
        self.switchBot.turn_off_switch()

    def _status(self):
        result = self.switchBot.get_device_info()
        try:
            self.logger.info("get switchbot status {},{}".format(result["firmware"], result["battery"]))
            payload = json.dumps(result)
            self.mqtt_client.publish_status(payload)
        except KeyError or TypeError:
            self.logger.warning("Failed get device info {}".format(result))
        except TypeError:
            self.logger.warning("Device info is type error. must be dict {}".format(result))
        except JSONDecodeError as e:
            self.logger.warning("Failed device info serialized to string by json.dumps ")
        # TODO NetWorkErrorHandling