# from sstpyg.comms import Communications

# def run():
#    print("CLIENT!!")
#    print("comms?", Communications)
#
from enum import Enum
import arcade


def get_server_info():
    return {
        AppState.REMAINING_KLINGONS: 10,
        AppState.REMAINING_DAYS: 10,
        AppState.SHIP_TOTAL_ENERGY: 10,
        AppState.SHIP_ENG_ENERGY: 10,
        AppState.SHIP_OK: True,
        AppState.SUBSYSTEM_TORPEDO: 20,
        AppState.SUBSYSTEM_PHASERS: 20,
        AppState.SUBSYSTEM_WARP_ENGINE: 20,
        AppState.SUBSYSTEM_SHIELD: 50,
        AppState.SUBSYSTEM_IMPULSE: 80,
    }


class LCARSColors(Enum):
    BLACK = arcade.color.BLACK
    ORANGE = arcade.color.ORANGE_PEEL
    BLUE = arcade.color.AIR_SUPERIORITY_BLUE
    RED = arcade.color.LAVA
    YELLOW = arcade.color.CANARY_YELLOW
    PURPLE = arcade.color.FRENCH_LILAC
    PINK = arcade.color.BAKER_MILLER_PINK
    LIGHT_BLUE = arcade.color.CADET_BLUE
    BEIGE = arcade.color.TAN
    WHITE = arcade.color.WHITE


# Ejemplo de uso:
class Division(Enum):
    COMMAND = "COMMAND"
    ENGINEERING = "ENGINEERING"
    TACTICAL = "TACTICAL"


class AppState(Enum):
    REMAINING_KLINGONS = "RMK"
    REMAINING_DAYS = "RMD"
    SHIP_TOTAL_ENERGY = "STE"
    SHIP_ENG_ENERGY = "SEE"
    SHIP_OK = "SOO"
    SUBSYSTEM_TORPEDO = "SST"
    SUBSYSTEM_PHASERS = "SSP"
    SUBSYSTEM_WARP_ENGINE = "SWE"
    SUBSYSTEM_SHIELD = "SSS"
    SUBSYSTEM_IMPULSE = "SSI"

    def __str__(self):
        return AppStateLabels[self.name].value


class AppStateLabels(Enum):
    REMAINING_KLINGONS = "Remaining Klingons"
    REMAINING_DAYS = "Remaining Days"
    SHIP_TOTAL_ENERGY = "Ship Total Energy"
    SHIP_ENG_ENERGY = "Ship Engine Energy"
    SHIP_OK = "Ship Status"
    SUBSYSTEM_TORPEDO = "Torpedos"
    SUBSYSTEM_PHASERS = "Phasers"
    SUBSYSTEM_WARP_ENGINE = "Warp Engine"
    SUBSYSTEM_SHIELD = "Shields"
    SUBSYSTEM_IMPULSE = "Impulse"


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "LCARS Template"


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BLACK
        arcade.load_font("Okuda.otf")

        self.stardate = arcade.Text(
            "", 250, 650, arcade.color.WHITE, 44, font_name="Okuda"
        )
        self.error_message = arcade.Text(
            "", 490, 310, LCARSColors.RED.value, 144, font_name="Okuda"
        )

        self.stardate.text = "STARDATE 41353.2"
        self.prompt = arcade.Text(
            "", 260, 35, arcade.color.WHITE, 44, font_name="Okuda"
        )

        self.status = arcade.Text(
            "",
            950,
            520,
            LCARSColors.ORANGE.value,
            20,
            font_name="Okuda",
            width=300,
            multiline=True,
        )
        self.text_input = ""
        self.show_grid = False
        self.show_lrs = False
        self.show_status = False
        self.show_error = False

    def setup(self):
        """Set up the game and initialize the variables."""

        # Create the sprite lists
        self.sprites = arcade.SpriteList()

        img = "lcars.jpg"
        self.bg_sprite = arcade.Sprite(img)
        self.bg_sprite.position = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.sprites.append(self.bg_sprite)

    def draw_map_grid(self):
        GRID_SIZE = 40
        GRID_LEFT = 260
        GRID_RIGHT = GRID_LEFT + GRID_SIZE * 8
        GRID_BOTTOM = 220
        GRID_TOP = GRID_BOTTOM + 40 * 8
        # Dibujar líneas verticales
        for x in range(GRID_LEFT, GRID_RIGHT + 1, GRID_SIZE):
            arcade.draw_line(x, GRID_BOTTOM, x, GRID_TOP, LCARSColors.BEIGE.value, 2)

        # Dibujar líneas horizontales
        for y in range(GRID_BOTTOM, GRID_TOP + 1, GRID_SIZE):
            arcade.draw_line(GRID_LEFT, y, GRID_RIGHT, y, LCARSColors.BEIGE.value, 2)

    def draw_lrs(self):
        GRID_SIZE = 40
        GRID_LEFT = 260
        GRID_RIGHT = GRID_LEFT + GRID_SIZE * 8
        GRID_BOTTOM = 220
        GRID_TOP = GRID_BOTTOM + 40 * 8
        # Dibujar líneas verticales
        for x in range(GRID_LEFT, GRID_RIGHT + 1, GRID_SIZE):
            arcade.draw_line(x, GRID_BOTTOM, x, GRID_TOP, LCARSColors.BEIGE.value, 2)

        # Dibujar líneas horizontales
        for y in range(GRID_BOTTOM, GRID_TOP + 1, GRID_SIZE):
            arcade.draw_line(GRID_LEFT, y, GRID_RIGHT, y, LCARSColors.BEIGE.value, 2)

    def draw_error_message(self):
        self.error_message.text = "ERROR"
        self.error_message.draw()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.sprites.draw()
        self.stardate.draw()
        self.prompt.draw()
        if self.show_grid:
            self.draw_map_grid()
        if self.show_lrs:
            self.draw_lrs()
        if self.show_status:
            self.draw_status()
        if self.show_error:
            self.draw_error_message()
        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        ...

    def draw_status(self):
        status_text = ""
        for key, value in get_server_info().items():
            status_text += f"{key}: {value}\n"
        self.status.text = "STATUS \n" + status_text
        self.status.draw()

    def show_text(self):
        self.prompt.text = self.text_input

    def process_command(self):
        self.show_error = False
        self.show_grid = False
        self.show_lrs = False
        self.show_status = False

        if self.text_input == "srs":
            self.show_grid = True
            self.show_status = True
        elif self.text_input == "lrs":
            self.show_lrs = True
            self.show_status = True
        else:
            self.show_error = True
        self.text_input = ""

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:

        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.RETURN:
            self.process_command()
        elif key == arcade.key.BACKSPACE:
            self.text_input = self.text_input[:-1]
        else:
            self.text_input += chr(key)
        self.show_text()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)
    game.setup()
    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
