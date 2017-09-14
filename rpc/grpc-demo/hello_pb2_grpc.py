# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import hello_pb2 as hello__pb2


class GreeterStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SayHello = channel.unary_unary(
        '/Greeter/SayHello',
        request_serializer=hello__pb2.HelloRequest.SerializeToString,
        response_deserializer=hello__pb2.HelloReply.FromString,
        )
    self.PlusTest = channel.unary_unary(
        '/Greeter/PlusTest',
        request_serializer=hello__pb2.PlusRequest.SerializeToString,
        response_deserializer=hello__pb2.PlusResponse.FromString,
        )


class GreeterServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def SayHello(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def PlusTest(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GreeterServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SayHello': grpc.unary_unary_rpc_method_handler(
          servicer.SayHello,
          request_deserializer=hello__pb2.HelloRequest.FromString,
          response_serializer=hello__pb2.HelloReply.SerializeToString,
      ),
      'PlusTest': grpc.unary_unary_rpc_method_handler(
          servicer.PlusTest,
          request_deserializer=hello__pb2.PlusRequest.FromString,
          response_serializer=hello__pb2.PlusResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Greeter', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))