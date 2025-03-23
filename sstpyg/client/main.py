import time
from pathlib import Path

import arcade
import threading

from sstpyg.client.constants import (
    LCARSColors,
    Division,
    AppState,
    AppStateLabels,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    GRID_RIGHT,
    GRID_BOTTOM,
    GRID_LEFT,
    GRID_SIZE,
    GRID_TOP,
)
from sstpyg.client.utils import srs_to_positions
from sstpyg.comms.client import ClientHandler


# Obtener el base path del archivo actual
BASE_PATH = Path(__file__).parent

# Hacer join con la carpeta "resources"
RESOURCES_PATH = BASE_PATH / "resources"


class RotatingList(list):
    def __str__(self):
        repr = [elem for elem in self]
        return "\n".join(repr[-5:])


class GameView(arcade.View):
    def __init__(self, server_address, role):
        super().__init__()
        self.server_address = server_address
        self.role = role

    def setup(self):
        """Set up the game and initialize the variables."""
        self.communication = ClientHandler(self.server_address, self.role)
        arcade.load_font(RESOURCES_PATH / "Okuda.otf")

        self.run_fetch_status = True

        # Sounds
        tng_bridge_sound = RESOURCES_PATH / "tng_bridge_1.mp3"
        self.sound_tng_bridge = arcade.load_sound(tng_bridge_sound)
        self.sound_tng_bridge.play(volume=0.3, loop=True)

        tng_key_sound = RESOURCES_PATH / "keyok2.mp3"
        self.beep_1 = arcade.load_sound(tng_key_sound)

        tng_process_sound = RESOURCES_PATH / "processing3.mp3"
        self.process_sound = arcade.load_sound(tng_process_sound)

        tng_error_sound = RESOURCES_PATH / "computer_error.mp3"
        self.error_sound = arcade.load_sound(tng_error_sound)

        # Common texts
        self.stardate = arcade.Text(
            "", 250, 660, arcade.color.WHITE, 44, font_name="Okuda"
        )
        self.error_message = arcade.Text(
            "",
            350,
            310,
            LCARSColors.RED.value,
            144,
            font_name="Okuda",
            align="center",
            width=500,
        )
        self.stardate.text = "STARDATE 41353.0"
        self.prompt = arcade.Text(
            "", 260, 35, arcade.color.WHITE, 44, font_name="Okuda"
        )
        self.status = arcade.Text(
            "",
            950,
            465,
            LCARSColors.ORANGE.value,
            22,
            font_name="Okuda",
            width=200,
            multiline=True,
        )

        self.location = arcade.Text(
            "", 680, 660, arcade.color.WHITE, 44, font_name="Okuda"
        )

        self.command_log = arcade.Text(
            "",
            950,
            175,
            LCARSColors.RED.value,
            24,
            font_name="Okuda",
            width=300,
            multiline=True,
        )

        self.text_input = ""
        self.show_grid = False
        self.show_lrs = False
        self.show_grs = False
        self.show_status = True
        self.show_error = False
        self.status_info = {}
        self.positions = []
        self.game_lost = False
        self.game_won = False
        self.enterprise_sector = ""
        self.enterprise_quadrant = ""

        # Background Sprite
        self.background = arcade.SpriteList()

        img = RESOURCES_PATH / "lcars.png"
        self.bg_sprite = arcade.Sprite(img)
        self.bg_sprite.position = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.background.append(self.bg_sprite)

        # Ship Sprites
        self.space_objects = arcade.SpriteList()

        self.command_log_history = RotatingList()

        galactic_registry = [["---" for x in range(0, 8)] for x in range(0, 8)]
        self.galactic_registry = galactic_registry

        lrs_registry = [["---" for x in range(0, 3)] for x in range(0, 3)]
        self.lrs_registry = lrs_registry

        self.start_fetch_status_task()

    def start_fetch_status_task(self):
        # Ejecuta la tarea asincrónica en un hilo separado
        thread = threading.Thread(target=self.fetch_status_task)
        self.thread = thread
        thread.start()

    def fetch_status_task(self):
        while self.run_fetch_status:
            self.status_info = self.communication.get_status()
            # Check a few things in the new info
            # Game over: energy 0, they destroy us, time over
            rem_energy = self.status_info[AppState.SHIP_TOTAL_ENERGY.value]
            shields = self.status_info[AppState.SUBSYSTEM_SHIELD.value]
            rem_days = self.status_info[AppState.REMAINING_DAYS.value]

            if not (rem_energy and shields and rem_days):
                self.game_lost = True
                self.run_fetch_status = False

            # Game won
            rem_klingons = self.status_info[AppState.REMAINING_KLINGONS.value]
            if not rem_klingons:
                self.game_won = True
                self.run_fetch_status = False

            time.sleep(0.4)

    def generate_space_object_sprite(self, img_file_name, coords, scale):
        img = RESOURCES_PATH / f"{img_file_name}.png"
        sprite = arcade.Sprite(img, scale=scale)
        sprite.position = coords

        self.space_objects.append(sprite)

    def place_sprites(self, img_file_name, set_of_coords, scale=0.030):
        for coords in set_of_coords:
            self.generate_space_object_sprite(
                img_file_name,
                (
                    GRID_LEFT + coords[0] * int(GRID_SIZE * 1.4) - (GRID_SIZE / 2),
                    GRID_TOP - coords[1] * GRID_SIZE + (GRID_SIZE / 2),
                ),
                scale,
            )

    def draw_map_grid(self):
        """Draw the map grid."""
        # Dibujar líneas verticales
        background = arcade.SpriteList()

        img = RESOURCES_PATH / "starfield.jpg"
        bg_sprite = arcade.Sprite(
            img,
            scale=0.25,
        )
        bg_sprite.position = ((WINDOW_WIDTH // 2) - 60, (WINDOW_HEIGHT // 2) - 40)
        background.append(bg_sprite)
        background.draw()

        k_positions, e_positions, s_positions, b_positions = srs_to_positions(
            self.positions
        )
        n_klingons = len(k_positions)
        n_starbases = len(b_positions)
        n_stars = len(s_positions)
        summary = str(n_klingons) + str(n_starbases) + str(n_stars)
        current_quadrant = self.status_info[AppState.ENTERPRISE_QUADRANT.value]

        self.galactic_registry[current_quadrant[1] - 1][current_quadrant[0] - 1] = (
            summary
        )
        light_blue_translucent = (173, 216, 230, 40)

        h_grid_number = 1
        while h_grid_number < 8:
            x = GRID_LEFT + h_grid_number * int(GRID_SIZE * 1.4)
            arcade.draw_line(x, GRID_BOTTOM, x, GRID_TOP, light_blue_translucent, 2)
            h_grid_number += 1

        v_grid_number = 1
        while v_grid_number < 8:
            y = GRID_BOTTOM + v_grid_number * int(GRID_SIZE)
            arcade.draw_line(GRID_LEFT, y, GRID_RIGHT, y, light_blue_translucent, 2)
            v_grid_number += 1

        arcade.draw_line(
            GRID_LEFT - 10,
            GRID_TOP,
            GRID_LEFT - 10,
            GRID_BOTTOM,
            LCARSColors.ORANGE.value,
            2,
        )

        arcade.draw_line(
            GRID_RIGHT + 10,
            GRID_TOP,
            GRID_RIGHT + 10,
            GRID_BOTTOM,
            LCARSColors.ORANGE.value,
            2,
        )

        for i in range(8):
            arcade.draw_text(
                str(i + 1),
                GRID_LEFT - 25,
                485 - (i * GRID_SIZE),
                LCARSColors.BLUE.value,
                14,
                font_name="Okuda",
            )
            arcade.draw_text(
                str(i + 1),
                GRID_RIGHT + 25,
                485 - (i * GRID_SIZE),
                LCARSColors.BLUE.value,
                14,
                font_name="Okuda",
            )
            arcade.draw_text(
                str(i + 1),
                GRID_LEFT + 34 + (i * GRID_SIZE * 1.40),
                530,
                LCARSColors.BLUE.value,
                14,
                font_name="Okuda",
            )

        # Mostrar naves
        self.space_objects.clear()

        self.place_sprites(
            "klingon_logo",
            k_positions,
        )
        self.place_sprites(
            "enterprise",
            e_positions,
        )
        self.place_sprites(
            "starfleet_logo",
            b_positions,
        )
        self.place_sprites(
            "star",
            s_positions,
        )

    def draw_lrs(self):
        """Draw the LRS."""

        current_quadrant = self.status_info[AppState.ENTERPRISE_QUADRANT.value]

        for i in range(3):
            for j in range(3):
                try:
                    x = current_quadrant[1] + (i - 1) - 1
                    y = current_quadrant[0] + (j - 1) - 1
                    if x < 0 or y < 0:
                        raise Exception
                    self.galactic_registry[x][y] = self.lrs_registry[i][j]
                except Exception:
                    pass
                arcade.Text(
                    self.lrs_registry[i][j],
                    440 + j * 100,
                    410 - i * 100,
                    LCARSColors.BEIGE.value,
                    72,
                    font_name="Okuda",
                    align="center",
                ).draw()

    def draw_grs(self):
        """Draw the GRS."""
        for i in range(8):
            for j in range(8):
                if i == 0:
                    arcade.Text(
                        str(j + 1),
                        340 + j * 70 + 20,
                        462 - (i - 1) * 50,
                        LCARSColors.BLUE.value,
                        20,
                        font_name="Okuda",
                    ).draw()
                if j == 0:
                    arcade.Text(
                        str(i + 1),
                        340 + j * 70 - 30,
                        462 - i * 50 + 10,
                        LCARSColors.BLUE.value,
                        20,
                        font_name="Okuda",
                    ).draw()

                arcade.Text(
                    self.galactic_registry[i][j],
                    340 + j * 70,
                    462 - i * 50,
                    LCARSColors.BEIGE.value,
                    40,
                    font_name="Okuda",
                ).draw()

    def draw_error_message(self, color=LCARSColors.RED.value, msg="ERROR"):
        """Draw error message."""
        self.reset_screen()
        self.error_message.text = msg
        self.error_message.color = color
        self.error_message.draw()

    def draw_status(self):
        """Draw status."""
        status_text = ""
        for key, value in self.status_info.items():
            if AppState(key) in Division.get_statuses(self.role):
                status_text += (
                    f"{getattr(AppStateLabels, AppState(key).name).value}: {value}\n"
                )
        self.status.text = "" + status_text
        self.status.draw()

    def draw_location(self):
        ent_quadrant = self.status_info[AppState.ENTERPRISE_POSITION.value]
        ent_sector = self.status_info[AppState.ENTERPRISE_QUADRANT.value]
        self.location.text = f"Quadrant: {ent_quadrant[0]}, {ent_quadrant[1]}        Sector:{ent_sector[0]}, {ent_sector[1]}"
        self.location.draw()

    def draw_command_log(self):
        """Draw command log."""
        self.command_log.text = self.command_log_history
        self.command_log.draw()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def reset_screen(self):
        self.clear()
        self.background.draw()
        self.stardate.draw()
        self.prompt.draw()
        self.draw_status()
        self.draw_location()
        self.draw_command_log()

    def on_draw(self):
        """
        Render the screen.
        """
        self.reset_screen()
        if self.show_grid:
            self.draw_map_grid()
            self.space_objects.draw()
        if self.show_lrs:
            self.draw_lrs()
        if self.show_grs:
            self.draw_grs()
        if self.show_error:
            self.draw_error_message()
        if self.game_lost:
            self.draw_error_message(msg="GAME OVER")
        if self.game_won:
            self.draw_error_message(msg="YOU WIN", color = LCARSColors.PURPLE.value)

    def draw_prompt(self):
        """Draw prompt."""
        self.prompt.text = self.text_input

    def process_command(self):
        """Process a command."""

        self.show_error = False
        self.show_grid = False
        self.show_lrs = False
        self.show_grs = False

        command = self.text_input[:3].lower()
        input = self.text_input

        try:
            if command == "srs":
                arcade.play_sound(self.process_sound, volume=0.5)
                self.positions = self.communication.command({"command": command})
                self.show_grid = True
            elif command == "lrs":
                arcade.play_sound(self.process_sound, volume=0.5)
                self.lrs_registry = self.communication.command({"command": command})
                self.show_lrs = True
            elif command == "tor":
                arcade.play_sound(self.process_sound, volume=0.5)
                self.communication.command({"command": command})
            elif command == "grs":
                arcade.play_sound(self.process_sound, volume=0.5)
                self.show_grs = True
            elif command in ["she", "pha"]:
                arcade.play_sound(self.process_sound, volume=0.5)
                _, energy = input.split(" ")
                self.communication.command(
                    {
                        "command": command,
                        "parameters": {"energy": energy},
                    }
                )
            elif command == "nav":
                arcade.play_sound(self.process_sound, volume=0.5)
                _, direction, warp_factor = input.split(" ")
                self.communication.command(
                    {
                        "command": command,
                        "parameters": {
                            "direction": direction,
                            "warp_factor": warp_factor,
                        },
                    }
                )
            elif command in ["dis", "rep"]:
                """ Permite asignar energía para el funcionamiento o reparación de cada subsistema """
                arcade.play_sound(self.process_sound, volume=0.5)
                _, subsystem, energy = input.split(" ")
                self.communication.command(
                    {
                        "command": command,
                        "parameters": {"subsystem": subsystem, "energy": energy},
                    }
                )
            elif command in [":q", ":wq", ":wq!", ":q!"]:
                arcade.play_sound(self.process_sound, volume=0.5)
                self.run_fetch_status = False
                self.thread.join()
                time.sleep(0.5)
                arcade.close_window()
            else:
                arcade.play_sound(self.error_sound, volume=2.2)
                self.show_error = True
                raise Exception
            self.command_log_history.append(command)
        except Exception:
            arcade.play_sound(self.error_sound, volume=2.2)
            self.show_error = True
        self.text_input = ""

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:

        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.ESCAPE:
            self.run_fetch_status = False
            self.thread.join()
            arcade.close_window()
        if key == arcade.key.RETURN:
            self.process_command()
        elif key == arcade.key.BACKSPACE:
            arcade.play_sound(self.beep_1, volume=0.5)
            self.text_input = self.text_input[:-1]
        elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            pass
        else:
            arcade.play_sound(self.beep_1, volume=0.5)
            self.text_input += chr(key)
        self.draw_prompt()


def run(server_address, role):
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView(server_address, role)

    # Show GameView on screen
    window.show_view(game)
    game.setup()

    # Start the arcade game loop
    arcade.run()
