from concurrent import futures

import time

import grpc

import hello_pb2
import hello_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(hello_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)

    def PlusTest(self, request, context):
        return hello_pb2.PlusResponse(result=request.num1+request.num2)

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except:
        server.stop(0)

if __name__ == '__main__':
    server()
