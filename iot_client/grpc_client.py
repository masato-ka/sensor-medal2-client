from logging import getLogger

import grpc

import sample_pb2
import sample_pb2_grpc
from config.config_manager import ConfigManager


class GrpcClient():

    logger = getLogger(__name__)
    _observer = None

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        ip = self.config_manager.options.grpc_ip
        port = self.config_manager.options.grpc_port
        channel = grpc.insecure_channel('{}:{}'.format(ip,port))
        self.stub = sample_pb2_grpc.RecordServiceStub(channel)

    def connect(self):
        result = self.stub.GetDeviceList(sample_pb2.RecordMessage(message=''))
        self._observer.notify(result.device_list)

    def setObserver(self, observer):
        self._observer = observer

    def publish_telemetry(self, message, subfolder=''):
        self.logger.info('publish telemetry message subfolder:{}, message:{}'.format(subfolder, message))
        self.stub.Record(sample_pb2.RecordMessage(message=message))

    def publish_status(self, message):
        self.logger.info('publish status message:{}'.format(message))