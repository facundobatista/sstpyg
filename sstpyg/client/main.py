from math import ceil
from pathlib import Path

import arcade
import asyncio
import threading

from sstpyg.client.constants import LCARSColors, Division, AppState, AppStateLabels
from sstpyg.client.utils import abs_coords_to_sector_coords, srs_to_positions
from sstpyg.client.mocks import srs
from sstpyg.comms.client import ClientHandler


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "SSTPYG"

GRID_SIZE = 40
GRID_LEFT = 260
GRID_RIGHT = GRID_LEFT + GRID_SIZE * 8
GRID_BOTTOM = 220
GRID_TOP = GRID_BOTTOM + GRID_SIZE * 8

# Obtener el base path del archivo actual
BASE_PATH = Path(__file__).parent

# Hacer join con la carpeta "resources"
RESOURCES_PATH = BASE_PATH / "resources"


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
        AppState.KLINGON_SHIPS_COORDS: [
            (1, 3),
            (6, 6),
            (8, 8),
            (1, 8),
        ],
        AppState.ENTERPRISE_POSITION: (1, 1),
        AppState.ENTERPRISE_QUADRANT: (1, 2),
    }


class GameView(arcade.View):
    def setup(self):
        """Set up the game and initialize the variables."""
        server_address = "192.168.111.23:8000"
        role = "capitan"
        self.communication = ClientHandler(server_address, role)
        self.background_color = arcade.color.BLACK
        arcade.load_font(RESOURCES_PATH / "Okuda.otf")

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
        self.show_grs = False
        self.show_status = False
        self.show_error = False

        # Create the sprite lists
        self.background = arcade.SpriteList()

        img = RESOURCES_PATH / "lcars.jpg"
        self.bg_sprite = arcade.Sprite(img)
        self.bg_sprite.position = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.background.append(self.bg_sprite)

        # Klingon ships
        self.space_objects = arcade.SpriteList()

        self.status_info = {}
        self.positions = []

        galactic_registry = [["---" for x in range(0, 9)] for x in range(0, 9)]

        self.galactic_registry = galactic_registry
        self.start_async_fetch_status_task()

    def start_async_fetch_status_task(self):
        # Ejecuta la tarea asincrónica en un hilo separado
        threading.Thread(target=self.fetch_status_task).start()

    def fetch_status_task(self):
        self.status_info = self.communication.get_status()

    def generate_klingon_sprite(self, coords):
        img = RESOURCES_PATH / "klingon_logo.png"
        klingon_sprite = arcade.Sprite(img, scale=0.040)
        klingon_sprite.position = coords

        self.space_objects.append(klingon_sprite)

    def generate_enterprise_sprite(self, coords):
        img = RESOURCES_PATH / "enterprise.png"
        enterprise_sprite = arcade.Sprite(img, scale=0.040)
        enterprise_sprite.position = coords

        self.space_objects.append(enterprise_sprite)

    def generate_starbase_sprite(self, coords):
        img = RESOURCES_PATH / "starfleet_logo.png"
        starbase_sprite = arcade.Sprite(img, scale=0.040)
        starbase_sprite.position = coords

        self.space_objects.append(starbase_sprite)

    def generate_star_sprite(self, coords):
        img = RESOURCES_PATH / "star.png"
        star_sprite = arcade.Sprite(img, scale=0.040)
        star_sprite.position = coords

        self.space_objects.append(star_sprite)

    def place_sprites(self, sprite_method, set_of_coords):
        for coords in set_of_coords:
            sector_coords = abs_coords_to_sector_coords(coords)
            sprite_method(
                (
                    GRID_LEFT + sector_coords[0] * GRID_SIZE - (GRID_SIZE / 2),
                    GRID_TOP - sector_coords[1] * GRID_SIZE + (GRID_SIZE / 2),
                )
            )

    def draw_map_grid(self):
        """Draw the map grid."""
        # Dibujar líneas verticales

        k_positions, e_positions, s_positions, b_positions = srs_to_positions(
            self.positions
        )
        n_klingons = len(k_positions)
        n_starbases = len(b_positions)
        n_stars = len(s_positions)
        summary = str(n_klingons) + str(n_starbases) + str(n_stars)
        current_quadrant = self.status_info[AppState.ENTERPRISE_QUADRANT]

        self.galactic_registry[current_quadrant[1] - 1][current_quadrant[0] - 1] = (
            summary
        )

        for x in range(GRID_LEFT, GRID_RIGHT + 1, GRID_SIZE):
            arcade.draw_line(x, GRID_BOTTOM, x, GRID_TOP, LCARSColors.BEIGE.value, 2)

        # Dibujar líneas horizontales
        for y in range(GRID_BOTTOM, GRID_TOP + 1, GRID_SIZE):
            arcade.draw_line(GRID_LEFT, y, GRID_RIGHT, y, LCARSColors.BEIGE.value, 2)

        # Mostrar naves klingon
        self.space_objects.clear()

        self.place_sprites(
            self.generate_klingon_sprite,
            k_positions,
        )
        self.place_sprites(
            self.generate_enterprise_sprite,
            e_positions,
        )
        self.place_sprites(
            self.generate_starbase_sprite,
            b_positions,
        )
        self.place_sprites(
            self.generate_star_sprite,
            s_positions,
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

    def draw_grs(self):
        """Draw the LRS."""
        for i in range(9):
            for j in range(9):
                arcade.draw_text(
                    self.galactic_registry[i][j],
                    340 + i * 50,
                    462 - j * 50,
                    LCARSColors.BEIGE.value,
                    40,
                    font_name="Okuda",
                )

    def draw_error_message(self):
        """Draw error message."""
        self.error_message.text = "ERROR"
        self.error_message.draw()

    def draw_status(self):
        """Draw status."""
        status_text = ""
        for key, value in self.status_info.items():
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
            self.space_objects.draw()
        if self.show_lrs:
            self.draw_lrs()
        if self.show_grs:
            self.draw_grs()
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
        self.show_grs = False

        if self.text_input == "srs":
            self.positions = self.communication.command({"command": "srs"})
            self.show_grid = True
            self.show_status = True
        elif self.text_input == "lrs":
            self.show_lrs = True
            self.show_status = True
        elif self.text_input == "grs":
            self.show_grs = True
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


def run():
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
