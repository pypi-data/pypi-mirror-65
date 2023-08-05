# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import wallet_pb2 as wallet__pb2


class WalletStub(object):
  """The service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateWallet = channel.unary_unary(
        '/wallet.Wallet/CreateWallet',
        request_serializer=wallet__pb2.Request.SerializeToString,
        response_deserializer=wallet__pb2.Response.FromString,
        )
    self.ViewWallet = channel.unary_unary(
        '/wallet.Wallet/ViewWallet',
        request_serializer=wallet__pb2.Request.SerializeToString,
        response_deserializer=wallet__pb2.Response.FromString,
        )
    self.RequestELA = channel.unary_unary(
        '/wallet.Wallet/RequestELA',
        request_serializer=wallet__pb2.Request.SerializeToString,
        response_deserializer=wallet__pb2.Response.FromString,
        )


class WalletServicer(object):
  """The service definition.
  """

  def CreateWallet(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ViewWallet(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RequestELA(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WalletServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateWallet': grpc.unary_unary_rpc_method_handler(
          servicer.CreateWallet,
          request_deserializer=wallet__pb2.Request.FromString,
          response_serializer=wallet__pb2.Response.SerializeToString,
      ),
      'ViewWallet': grpc.unary_unary_rpc_method_handler(
          servicer.ViewWallet,
          request_deserializer=wallet__pb2.Request.FromString,
          response_serializer=wallet__pb2.Response.SerializeToString,
      ),
      'RequestELA': grpc.unary_unary_rpc_method_handler(
          servicer.RequestELA,
          request_deserializer=wallet__pb2.Request.FromString,
          response_serializer=wallet__pb2.Response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'wallet.Wallet', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
