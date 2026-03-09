import asyncio, traceback

from network.connection import Connection

class TcpServer:    
    def __init__(self, addr):
        self.addr = addr

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info("peername")
        print(f"new connection from {addr[0]}:{addr[1]}")

        con = Connection(reader, writer)

        try:
            while True:
                result = await con.receive_message()

                if result == -1:
                    break
        except asyncio.exceptions.IncompleteReadError:
            pass
        except ConnectionResetError:
            pass
        except Exception as e:
            # for debugging
            traceback.print_exc()
            pass

        print("disconnect!")

        try:
            writer.close()
            await writer.wait_closed()
        except: 
            pass

    async def start_accept(self):
        server = await asyncio.start_server(
            self.handle_client,
            self.addr[0],
            self.addr[1]
        )

        print("TCP server started!")

        async with server:
            await server.serve_forever()
    
    async def main():
        server = TcpServer(('0.0.0.0', 9339))
        await server.start_accept()