import asyncio

from sstpyg.comms.client import ClientHandler


def run(server_address, role_param):
    print("CLIENT!!")

    client = ClientHandler(server_address=server_address)
    print(asyncio.run(client.initialize(role_param)))
    command_params = {"action": "attack", "position": [1, 2]}
    print(asyncio.run(client.command(command_params)))
