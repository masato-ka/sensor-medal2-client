from logging import getLogger

import grpc

import sample_pb2
import sample_pb2_grpc


class GrpcClient():

    logger = getLogger(__name__)
    _observer = None

    def __init__(self):
        channel = grpc.insecure_channel('192.168.10.8:50051')
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