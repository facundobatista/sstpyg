class GameEngine:
    def initialize(self, role):
        message = f"Initialize {role} received!"
        print(message)

        return message

    def command(self, command_body):
        message = f"Command received! {command_body}"
        print(message)

        # tmp: fix this
        from sstpyg.client.mocks import srs, lrs

        if command_body["command"] == "srs":
            message = srs()
        elif command_body["command"] == "lrs":
            message = lrs()
        return message

    def get_status(self):
        message = "Get status received!"
        print(message)

        # tmp: fix this
        from sstpyg.client.mocks import get_server_info

        message = get_server_info()

        return message
