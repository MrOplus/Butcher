from socketserver import ThreadingUDPServer
from .PacketHandler import PacketHandler
from config import RuntimeConfig

class DNSServer:
    def __init__(self) -> None:
        super().__init__()

    def get_server(self):
        return self.server

    def run_for_ever(self):
        try:
            address = (RuntimeConfig.network()['address'], RuntimeConfig.network()['port'])
            self.server = ThreadingUDPServer(address, PacketHandler)
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Keyboard Interrupt, Exiting ...")
        except OSError:
            print("Port in-use")
