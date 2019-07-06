import json
from json import JSONDecodeError

from device.sensor_medal import SensorMedal
from iot_client.cloud_iot_core import CloudIoTCoreClient


class ClientController:
    def __init__(self, mqtt_client: CloudIoTCoreClient, sensor_medal: SensorMedal):
        self.event = None

        self.mqtt_client = mqtt_client
        self.mqtt_client.setObserver(self)
        self.sensor_medal = sensor_medal

    def start(self):
        self.mqtt_client.connect()

    def notify(self, event):
        self.logger.debug("Get event from IoT Core: {}".format(event))
        event_map = json.loads(event)
        self._event_router(event_map)

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