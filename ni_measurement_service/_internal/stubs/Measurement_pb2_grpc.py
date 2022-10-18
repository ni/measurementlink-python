# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ni_measurement_service._internal.stubs import Measurement_pb2 as Measurement__pb2


class MeasurementServiceStub(object):
    """Service that contains methods related to measurement"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetMetadata = channel.unary_unary(
            "/ni.measurements.v1.MeasurementService/GetMetadata",
            request_serializer=Measurement__pb2.GetMetadataRequest.SerializeToString,
            response_deserializer=Measurement__pb2.GetMetadataResponse.FromString,
        )
        self.Measure = channel.unary_unary(
            "/ni.measurements.v1.MeasurementService/Measure",
            request_serializer=Measurement__pb2.MeasureRequest.SerializeToString,
            response_deserializer=Measurement__pb2.MeasureResponse.FromString,
        )


class MeasurementServiceServicer(object):
    """Service that contains methods related to measurement"""

    def GetMetadata(self, request, context):
        """API to get complete metadata"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Measure(self, request, context):
        """API to measure"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_MeasurementServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetMetadata": grpc.unary_unary_rpc_method_handler(
            servicer.GetMetadata,
            request_deserializer=Measurement__pb2.GetMetadataRequest.FromString,
            response_serializer=Measurement__pb2.GetMetadataResponse.SerializeToString,
        ),
        "Measure": grpc.unary_unary_rpc_method_handler(
            servicer.Measure,
            request_deserializer=Measurement__pb2.MeasureRequest.FromString,
            response_serializer=Measurement__pb2.MeasureResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "ni.measurements.v1.MeasurementService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class MeasurementService(object):
    """Service that contains methods related to measurement"""

    @staticmethod
    def GetMetadata(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/ni.measurements.v1.MeasurementService/GetMetadata",
            Measurement__pb2.GetMetadataRequest.SerializeToString,
            Measurement__pb2.GetMetadataResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Measure(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/ni.measurements.v1.MeasurementService/Measure",
            Measurement__pb2.MeasureRequest.SerializeToString,
            Measurement__pb2.MeasureResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
