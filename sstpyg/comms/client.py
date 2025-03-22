import httpx


class ClientHandler:
    def __init__(self, server_address):
        """
        Server address is a combination of the host and port.
        """
        self.server_address = server_address
        self.client = httpx.AsyncClient()

    async def initialize(self, role):
        """
        Send a GET request to the server.
        """
        response = await self.client.get(f"http://{self.server_address}/initialize/{role}")
        return response.text


    async def command(self, command_params):
        """
        Send a POST request to the server.
        """
        response = await self.client.post(f"http://{self.server_address}/command", json=command_params)
        return response.text
