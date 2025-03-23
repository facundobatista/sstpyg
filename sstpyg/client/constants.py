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
    COMMAND = "CAPTAIN"
    ENGINEERING = "ENGINEERING"
    TACTICAL = "TACTICAL"

    @classmethod
    def get_statuses(cls, role):
        mapping = {
            cls.COMMAND.value.lower(): [
                AppState.REMAINING_KLINGONS,
                AppState.REMAINING_DAYS,
                AppState.SHIP_TOTAL_ENERGY,
                AppState.SHIP_OK,
            ],
            cls.ENGINEERING.value.lower(): [
                AppState.SHIP_ENG_ENERGY,
                AppState.SHIP_TOTAL_ENERGY,
                AppState.SUBSYSTEM_TORPEDO,
                AppState.SUBSYSTEM_PHASERS,
                AppState.SUBSYSTEM_WARP_ENGINE,
                AppState.SUBSYSTEM_SHIELD,
                AppState.SUBSYSTEM_IMPULSE,
            ],
            cls.TACTICAL.value.lower(): [
                AppState.SUBSYSTEM_TORPEDO,
                AppState.SUBSYSTEM_PHASERS,
                AppState.SUBSYSTEM_SHIELD,
            ],
        }
        return mapping[role]


class AppState(Enum):
    REMAINING_KLINGONS = "RMK"
    REMAINING_DAYS = "RMD"
    SHIP_TOTAL_ENERGY = "STE"
    SHIP_OK = "SOO"
    SHIP_ENG_ENERGY = "SEE"
    SUBSYSTEM_TORPEDO = "SST"
    SUBSYSTEM_PHASERS = "SSP"
    SUBSYSTEM_WARP_ENGINE = "SWE"
    SUBSYSTEM_SHIELD = "SSS"
    SUBSYSTEM_IMPULSE = "SSI"
    KLINGON_SHIPS_COORDS = "KSC"
    ENTERPRISE_POSITION = "EPOS"
    ENTERPRISE_QUADRANT = "EQUAD"


CAPITAN_STATUSES = [
    AppState.REMAINING_KLINGONS,
    AppState.REMAINING_DAYS,
    AppState.SHIP_TOTAL_ENERGY,
    AppState.SHIP_OK,
]


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
    ENTERPRISE_POSITION = "Enterprise"
    ENTERPRISE_QUADRANT = "Enterprise Quadrant"


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "LCARS Template"

GRID_SIZE = 50
GRID_LEFT = 300
GRID_RIGHT = GRID_LEFT + GRID_SIZE * 8 * 1.4
GRID_BOTTOM = 120
GRID_TOP = GRID_BOTTOM + GRID_SIZE * 8
