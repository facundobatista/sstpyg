import asyncio
import random
from dataclasses import dataclass

from sstpyg.comms import Communications
from sstpyg.server.safemap import SafeMap


def run():
    print("SERVER!!")
    print("comms?", Communications)


KLINGON = "(K)"
ENTERPRISE = ":E:"
EMPTY = "---"
STAR = " * "
BASE = "[@]"
OUTGALAXY = "***"


@dataclass
class State:
    loc_quadrant: tuple[int, int]
    loc_sector: tuple[int, int]
    remaining_energy: int = random.randint(2500, 3000)
    remaining_days: int = random.randint(900, 1500)
    remaining_klingons: int = random.randint(10, 20)
    remaining_torpedoes: int = random.randint(8, 12)
    subs_torpedoes: int = 1
    subs_phasers: int = 1
    subs_warp: int = 1
    subs_impulse: int = 1
    subs_shields: int = 1


class Engine:
    cant_stars_total = random.randint(40, 60)
    cant_bases_total = random.randint(2, 5)
    enterprise_loc = ()

    def __init__(self):

        # the galaxy map is 8x8, where each item there is another map 8x8
        self.mapa = SafeMap(8, 8, out_of_map=OUTGALAXY)
        for x in range(8):
            for y in range(8):
                self.mapa[(x, y)] = SafeMap(8, 8, fill=EMPTY)

        self._fill_map(KLINGON, State.remaining_klingons)
        self._fill_map(STAR, self.cant_stars_total)
        self._fill_map(BASE, self.cant_bases_total)

        (enterprise_position,) = self._fill_map(ENTERPRISE, 1)
        loc_quadrant, loc_sector = enterprise_position

        self.state = State(loc_quadrant=loc_quadrant, loc_sector=loc_sector)

    def _fill_map(self, item, quantity):
        positions = []
        while quantity:
            qx, qy, sx, sy = [random.randrange(8) for _ in range(4)]
            if self.mapa[(qx, qy)][(sx, sy)] == EMPTY:
                self.mapa[(qx, qy)][(sx, sy)] = item
                positions.append(((qx, qy), (sx, sy)))
                quantity -= 1
        return positions

    async def init(self):
        self.loop = asyncio.get_event_loop()
        self.repeat(5, self.klingon_ai)
        self.repeat(1, self.time_goes_by)

    def repeat(self, delay, func, first=True):
        loop = asyncio.get_event_loop()
        if not first:
            func()
        loop.call_later(delay, self.repeat, delay, func, False)

    def klingon_ai(self):
        print("========== klingon attack!!")

    def time_goes_by(self):
        self.state.remaining_energy -= 1

    async def get_state(self):
        return self.state

    async def command(self, command):
        match command:
            case "srs":
                result = await self.cmd_srs()
            case "lrs":
                result = await self.cmd_lrs()
            case _:
                result = f"ERROR: bad command {command!r}"
        return result

    async def get_galaxy(self, coords):
        if coords is not None:
            return self.mapa[coords]
        else:
            return self.mapa

    async def cmd_srs(self):
        return self.mapa[self.state.loc_quadrant]

    def _quadrant_summary(self, quadrant):
        cant_klingon = 0
        cant_stars = 0
        cant_bases = 0
        for objeto in quadrant.walk():
            if objeto == KLINGON:
                cant_klingon += 1
            elif objeto == STAR:
                cant_stars += 1
            elif objeto == BASE:
                cant_bases += 1
        return cant_klingon, cant_bases, cant_stars

    async def cmd_lrs(self):
        qx, qy = self.state.loc_quadrant
        result = []
        for dx in (-1, 0, +1):
            row = []
            for dy in (-1, 0, +1):
                quadrant = self.mapa[(qx + dx, qy + dy)]
                row.append(self._quadrant_summary(quadrant))
            result.append(row)
        return result
