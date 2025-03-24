import asyncio
import math
import random
from dataclasses import dataclass, asdict

from sstpyg.server.safemap import SafeMap

KLINGON = "K"
ENTERPRISE = "E"
EMPTY = ""
STAR = "S"
BASE = "B"
OUTGALAXY = "***"


ENERGYUSE_REGULAR = 1
ENERGYUSE_MOVE_SUBLIGHT = 2
ENERGYUSE_MOVE_WARP = 20
ENERGYUSE_COLLISION = 50


@dataclass
class State:
    loc_quadrant: tuple[int, int]
    loc_sector: tuple[int, int]
    remaining_energy: int = random.randint(2500, 3000)
    remaining_days: float = random.randint(15, 25)
    remaining_klingons: int = random.randint(10, 20)
    remaining_torpedoes: int = random.randint(8, 12)
    subs_torpedoes: int = 1
    subs_phasers: int = 1
    subs_warp: int = 1
    subs_impulse: int = 1
    subs_shields: int = 1
    docked: bool = False


class Engine:
    cant_stars_total = random.randint(40, 60)
    cant_bases_total = random.randint(2, 5)
    enterprise_loc = ()

    def __init__(self):

        # the galaxy map is 8x8, where each item there is another map 8x8
        self.gxmap = SafeMap(8, 8, out_of_map=None)
        for x in range(8):
            for y in range(8):
                self.gxmap[(x, y)] = SafeMap(8, 8, fill=EMPTY, out_of_map=None)

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
            if self.gxmap[(qx, qy)][(sx, sy)] == EMPTY:
                self.gxmap[(qx, qy)][(sx, sy)] = item
                positions.append(((qx, qy), (sx, sy)))
                quantity -= 1
        return positions

    async def init(self):
        self.loop = asyncio.get_event_loop()
        self.repeat(5, self.klingon_ai)
        self.repeat(1, self.time_goes_by)

    async def add_client(self, role):
        print("====== add client", repr(role))
        # FIXME implement!

    def repeat(self, delay, func, first=True):
        loop = asyncio.get_event_loop()
        if not first:
            func()
        loop.call_later(delay, self.repeat, delay, func, False)

    def klingon_ai(self):
        """Called every 5 seconds."""
        # FIXME implement!

    def time_goes_by(self):
        """Called once per second."""
        # FIXME: support the Enterprise being "docked"
        self.state.remaining_energy -= ENERGYUSE_REGULAR

        # a "mission day" ~= 1 real minute; so once per second we reduce it in 1/60
        self.state.remaining_days -= 1 / 60

    async def get_state(self):
        return asdict(self.state)

    async def command(self, command_info):
        command = command_info["command"]
        meth_name = f"cmd_{command}"
        meth = getattr(self, meth_name, None)
        if meth is None:
            return f"ERROR: missing command: {command!r}"

        # FIXME: nav, dam, rep, dis, pha, she, tor
        parameters = command_info.get("parameters", {})
        try:
            return await meth(**parameters)
        except TypeError:
            return f"ERROR: bad parameters: {parameters}"

    async def get_galaxy(self, coords):
        if coords is not None:
            return self.gxmap[coords]
        else:
            return self.gxmap

    def move_enterprise_intraquadrant(self, quadrant_coords, src_sector, dest_sector):
        print("======= move enterprise intra", quadrant_coords, src_sector, dest_sector)
        # state
        self.state.loc_sector = dest_sector

        # move the enterprise from the map itself
        quadrant = self.gxmap[quadrant_coords]
        assert quadrant[src_sector] == ENTERPRISE
        quadrant[src_sector] = EMPTY
        assert quadrant[dest_sector] == EMPTY
        quadrant[dest_sector] = ENTERPRISE

    def move_enterprise_interquadrant(self, src_quadrant, src_sector, dest_quadrant):
        print("======= move enterprise inter", src_quadrant, src_sector, dest_quadrant)
        # find a place in the new quadrant
        new_quadrant = self.gxmap[dest_quadrant]
        while True:
            sx, sy = [random.randrange(8) for _ in range(2)]
            if new_quadrant[(sx, sy)] == EMPTY:
                break

        # state
        self.state.loc_sector = (sx, sy)
        self.state.loc_quadrant = dest_quadrant

        # move the enterprise from the map itself
        assert self.gxmap[src_quadrant][src_sector] == ENTERPRISE
        self.gxmap[src_quadrant][src_sector] = EMPTY
        new_quadrant[(sx, sy)] = ENTERPRISE

    def _nav_sublight(self, direction, warp_factor):
        quadrant = self.gxmap[self.state.loc_quadrant]

        src_x, src_y = self.state.loc_sector
        delta = warp_factor / 2  # 0.9 -> 0.45, 10 steps -> 4.5 cells, ~half sector
        dx = delta * math.cos(math.radians(direction))
        dy = -delta * math.sin(math.radians(direction))  # negative as Y goes down

        walked = {(src_x, src_y)}
        messages = []
        prv_x, prv_y = src_x, src_y
        for step in range(1, 11):
            nx = int(round(src_x + dx * step))
            ny = int(round(src_y + dy * step))
            if (nx, ny) in walked:
                continue
            walked.add((nx, ny))
            found = quadrant[(nx, ny)]

            if found == EMPTY:
                # normal situation
                messages.append(f"Moved into ({nx}, {ny})")
                self.move_enterprise_intraquadrant(
                    self.state.loc_quadrant,
                    (prv_x, prv_y),
                    (nx, ny),
                )
                self.state.remaining_energy -= ENERGYUSE_MOVE_SUBLIGHT
                prv_x, prv_y = nx, ny
                continue

            # something weird happened
            if found == KLINGON:
                messages.append("Bumped into a Klingon ship! Damage!")
                self.state.remaining_energy -= ENERGYUSE_COLLISION
                # FIXME: break subsystem?
            elif found == STAR:
                messages.append("Bumped into a Star! Damage!")
                self.state.remaining_energy -= ENERGYUSE_COLLISION
                # FIXME: break subsystem?
            elif found == BASE:
                messages.append("Docked into a star base")
                self.state.docked = True
            elif found is None:
                dqx = nx - prv_x
                dqy = ny - prv_y
                qx, qy = self.state.loc_quadrant
                nqx = qx + dqx
                nqy = qy + dqy
                if self.gxmap[(nqx, nqy)] is None:
                    # new quadrant does not really exists
                    messages.append("Reached the limit of the galaxy!")
                else:
                    messages.append(f"Jumping to quadrant ({nqx}, {nqy})")
                    self.move_enterprise_interquadrant(
                        self.state.loc_quadrant,
                        (prv_x, prv_y),
                        (nqx, nqy),
                    )
                self.state.remaining_energy -= ENERGYUSE_MOVE_WARP

                # reaching here after any of weird situations, which imply stop moving
                break

            else:
                raise ValueError("Bug! Server bad move")
        return messages

    def _nav_warp(self, direction, warp_factor):
        src_x, src_y = self.state.loc_quadrant
        self.state.remaining_energy -= ENERGYUSE_MOVE_WARP * warp_factor

        dx = warp_factor * math.cos(math.radians(direction))
        dy = -warp_factor * math.sin(math.radians(direction))  # negative as Y goes down

        nx = src_x + int(round(dx))
        ny = src_y + int(round(dy))
        found = self.gxmap[(nx, ny)]
        if found is None:
            return ["Too fast, out of the galaxy, Q brought you back out of pity"]

        self.move_enterprise_interquadrant(
            self.state.loc_quadrant,
            self.state.loc_sector,
            (nx, ny),
        )
        return [f"Warping to quadrant ({nx}, {ny})"]

    async def cmd_nav(self, direction, warp_factor):
        print("======== nav!!", direction, warp_factor)
        if warp_factor < 1:
            return self._nav_sublight(direction, warp_factor)
        else:
            return self._nav_warp(direction, warp_factor)

    async def cmd_srs(self):
        quadrant = self.gxmap[self.state.loc_quadrant]
        return quadrant.serialize()

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
        for dy in (-1, 0, +1):
            row = []
            for dx in (-1, 0, +1):
                coords = (qx + dx, qy + dy)
                quadrant = self.gxmap[coords]
                if quadrant is None:
                    # out of galaxy
                    summary = "***"
                else:
                    values = self._quadrant_summary(quadrant)
                    # top values to 9
                    values = [value if value <= 9 else 9 for value in values]
                    summary = "".join(map(str, values))
                row.append(summary)
            result.append(row)
        return result
