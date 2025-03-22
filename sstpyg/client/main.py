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
        AppState.KLINGON_SHIPS_COORDS: [(1, 3), (6, 6)],
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
    KLINGON_SHIPS_COORDS = "KSC"

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
    KLINGON_SHIPS_COORDS = "KSC"


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "LCARS Template"

GRID_SIZE = 40
GRID_LEFT = 260
GRID_RIGHT = GRID_LEFT + GRID_SIZE * 8
GRID_BOTTOM = 220
GRID_TOP = GRID_BOTTOM + 40 * 8


class GameView(arcade.View):
    def setup(self):
        """Set up the game and initialize the variables."""
        self.background_color = arcade.color.BLACK
        arcade.load_font("Okuda.otf")

        self.stardate = arcade.Text(
            "", 250, 650, arcade.color.WHITE, 44, font_name="Okuda"
        )
        self.error_message = arcade.Text(
            "", 590, 310, LCARSColors.RED.value, 144, font_name="Okuda"
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

        # Create the sprite lists
        self.background = arcade.SpriteList()

        img = "lcars.jpg"
        self.bg_sprite = arcade.Sprite(img)
        self.bg_sprite.position = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.background.append(self.bg_sprite)

        # Klingon ships
        self.klingon_ships = arcade.SpriteList()

        # Klingon ships
        self.starbases = arcade.SpriteList()

    def generate_klingon_sprite(self, coords):
        img = "klingon_logo.png"
        klingon_sprite = arcade.Sprite(img, scale=0.040)
        klingon_sprite.position = coords

        self.klingon_ships.append(klingon_sprite)

    def generate_starbases_sprite(self, coords):
        img = "starfleet_logo.png"
        starbase_sprite = arcade.Sprite(img, scale=0.040)
        starbase_sprite.position = coords

        self.starbases.append(starbase_sprite)

    def place_sprites(self, sprite_method, set_of_coords):
        for coords in set_of_coords:
            actor_sprite = sprite_method(
                (
                    GRID_LEFT + coords[0] * GRID_SIZE - 20,
                    GRID_BOTTOM + coords[1] * GRID_SIZE - 20,
                )
            )

    def draw_map_grid(self):
        """Draw the map grid."""
        # Dibujar líneas verticales
        for x in range(GRID_LEFT, GRID_RIGHT + 1, GRID_SIZE):
            arcade.draw_line(x, GRID_BOTTOM, x, GRID_TOP, LCARSColors.BEIGE.value, 2)

        # Dibujar líneas horizontales
        for y in range(GRID_BOTTOM, GRID_TOP + 1, GRID_SIZE):
            arcade.draw_line(GRID_LEFT, y, GRID_RIGHT, y, LCARSColors.BEIGE.value, 2)

        # Mostrar naves klingon
        self.place_sprites(
            self.generate_klingon_sprite,
            get_server_info()[AppState.KLINGON_SHIPS_COORDS],
        )

    def draw_lrs(self):
        """Draw the LRS."""
        for i in range(3):
            arcade.draw_text(
                "000 001 002",
                400,
                432 - i * 80,
                LCARSColors.BEIGE.value,
                70,
                font_name="Okuda",
            )

    def draw_error_message(self):
        """Draw error message."""
        self.error_message.text = "ERROR"
        self.error_message.draw()

    def draw_status(self):
        """Draw status."""
        status_text = ""
        for key, value in get_server_info().items():
            status_text += f"{key}: {value}\n"
        self.status.text = "STATUS \n" + status_text
        self.status.draw()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.background.draw()
        self.stardate.draw()
        self.prompt.draw()
        if self.show_grid:
            self.draw_map_grid()
            self.klingon_ships.draw()
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

    def draw_prompt(self):
        """Draw prompt."""
        self.prompt.text = self.text_input

    def process_command(self):
        """Process a command."""
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
        self.draw_prompt()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
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
