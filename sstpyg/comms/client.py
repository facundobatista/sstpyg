import asyncio
import sys
import httpx


class ClientHandler:
    def __init__(self, server_address):
        """
        Server address is a combination of the host and port.
        """
        self.server_address = server_address
        self.client = httpx.AsyncClient()

    async def ping(self):
        """
        Send a GET request to the server.
        """
        response = await self.client.get(f"http://{self.server_address}/ping")
        return response.text


    async def command(self):
        """
        Send a POST request to the server.
        """
        response = await self.client.post(f"http://{self.server_address}/command")
        return response.text



if __name__ == "__main__":
    server_address = sys.argv[1]
    print(f"Received parameter: {server_address}")

    client = ClientHandler(server_address=server_address)
    print(asyncio.run(client.ping()))
    print(asyncio.run(client.command()))

