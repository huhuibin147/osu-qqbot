import sys,traceback,Ice

Ice.loadSlice("./hello.ice")

import Demo

class HelloI(Demo.Hello):
    def printer(self, s, current=None):
        return s

class Server(Ice.Application):
    def run(self, args):
        adapter = self.communicator().createObjectAdapter("Hello")
        adapter.add(HelloI(), Ice.stringToIdentity('hello'))
        adapter.activate()
        self.communicator().waitForShutdown()
        return 0

sys.stdout.flush()
app = Server()
sys.exit(app.main(sys.argv, "config.server"))


###############################


# status = 0
# ic = None
# try:
#     ic = Ice.initialize(sys.argv)

#     adapter=ic.createObjectAdapterWithEndpoints("SimplePrintAdapter","default -p 10000")
#     object = HelloI()
#     adapter.add(object, ic.stringToIdentity("SimplePrint"))
#     adapter.activate()
#     ic.waitForShutdown()
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