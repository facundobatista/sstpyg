import json

import httpx


class ClientHandler:
    def __init__(self, server_address, role):
        """
        Server address is a combination of the host and port.
        """
        self.server_address = server_address
        self.async_client = httpx.AsyncClient()
        self.sync_client = httpx.Client()
        self._initialize(role)

    def _initialize(self, role):
        """
        Initialize a client in the server with a specific role.
        """
        response = self.sync_client.get(f"http://{self.server_address}/initialize/{role}")
        try:
            return response.json()
        except json.JSONDecodeError:
            pass

        return response.text


    def command(self, command_params):
        """
        Send a command to the server. Command params must be a serializable dictionary.
        """
        response = self.sync_client.post(f"http://{self.server_address}/command", json=command_params)
        try:
            return response.json()
        except json.JSONDecodeError:
            pass

        return response.text


    async def async_status(self):
        """
        Get status from server.
        """
        response = await self.async_client.get(f"http://{self.server_address}/command")
        try:
            return response.json()
        except json.JSONDecodeError:
            pass

        return response.text
