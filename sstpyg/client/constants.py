from enum import Enum
import arcade


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
