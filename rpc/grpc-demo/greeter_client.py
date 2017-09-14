
import grpc

import hello_pb2
import hello_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = hello_pb2_grpc.GreeterStub(channel)
    # reponse = stub.SayHello(hello_pb2.HelloRequest(name='you'))
    # print(reponse.message)
    reponse = stub.PlusTest(hello_pb2.PlusRequest(num1=1, num2=2))
    print(reponse.result)

if __name__ == '__main__':
    run()

