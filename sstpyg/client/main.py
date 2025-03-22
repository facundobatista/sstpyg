# from sstpyg.comms import Communications

# def run():
#    print("CLIENT!!")
#    print("comms?", Communications)
#
from enum import Enum
import arcade


def get_server_info():
    return {
        AppState.REMAINING_KLINGONS.value: 10,
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
        return self.value


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

        self.status = arcade.Text(
            "",
            950,
            520,
            arcade.color.MAGENTA,
            24,
            font_name="Okuda",
            width=300,
            multiline=True,
        )

        # If you have sprite lists, you should create them here,
        # and set them to None
        #

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
            arcade.draw_line(x, GRID_BOTTOM, x, GRID_TOP, arcade.color.RED, 2)

        # Dibujar líneas horizontales
        for y in range(GRID_BOTTOM, GRID_TOP + 1, GRID_SIZE):
            arcade.draw_line(GRID_LEFT, y, GRID_RIGHT, y, arcade.color.RED, 2)

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
        self.status.draw()
        self.draw_map_grid()
        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.stardate.text = "STARDATE 41353.2"
        self.status.text = "STATUS: \n" + str(get_server_info())

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        arcade.close_window()

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
