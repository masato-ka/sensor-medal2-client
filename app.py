import os
import time
import logging
from client_controller import ClientController
from config.config_manager import ConfigManager
from device.sensor_medal import SensorMedal, MedalManager
from iot_client.cloud_iot_core import CloudIoTCoreClient
from iot_client.grpc_client import GrpcClient

logger = logging.getLogger(__name__)


def setting_logger():
    fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)





if __name__ == '__main__':
    setting_logger()
    config_manager = ConfigManager(os.path.dirname(os.path.abspath(__file__)))
    medal_manager = MedalManager()
    grpc_client = GrpcClient()
    iot_core_client = CloudIoTCoreClient(config_manager)
    #client_controller = ClientController(iot_core_client, medal_manager)
    client_controller = ClientController(grpc_client, medal_manager)
    client_controller.start()
    logger.info("start up switchbot hub")

    #iot_core_client = CloudIoTCoreClient(config_manager, medal_manager)
    #iot_core_client.connect()
    # while True:
    #
    #     time.sleep(5)
    #     medals = medal_manager.get_medal_data(['ROHMMedal2_0073_01.00'])
    #     for medal in medals:
    #         print(medal)
    #         print(check_status(medal))