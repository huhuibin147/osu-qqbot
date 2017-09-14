import sys,traceback,Ice

import Demo

# status = 0
# ic = None
# try:
#     ic = Ice.initialize(sys.argv)
#     base= ic.stringToProxy("hello:default -p 10000")
#     printer = Demo.HelloPrx.checkedCast(base)
#     if not printer:
#         raise RuntimeError("invaild proxy")

#     print(printer.printer("hello world!"))
# except:
#     traceback.print_exc()
#     status = 1

# if ic:
#     try:
#         ic.destroy()
#     except:
#         traceback.print_exc()
#         status=1

# sys.exit(status)

######################

def run(communicator):
    base = communicator.propertyToProxy('Hello.Proxy')
    printer = Demo.HelloPrx.checkedCast(base)
    if not printer:
        raise RuntimeError("invaild proxy")
    print(printer.printer('hello world!'))
    return 0


status = 0
with Ice.initialize(sys.argv, "config.client") as communicator:
    status = run(communicator)
sys.exit(status)