class GameEngine:
    def initialize(self, role):
        message = f"Initialize {role} received!"
        print(message)

        return message

    def command(self, command_body):
        message = f"Command received! {command_body}"
        print(message)
        return message

    def get_status(self):
        message = "Get status received!"
        print(message)
        return message
