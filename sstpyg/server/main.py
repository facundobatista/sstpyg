import asyncio
import random

from sstpyg.comms import Communications


def run():
    print("SERVER!!")
    print("comms?", Communications)


class Engine:
    cant_klingon_total = random.randint(10, 20)
    cant_stars_total = random.randint(40, 60)
    cant_starbases_total = random.randint(2, 5)
    cant_torpedoes = random.randint(8, 12)
    tiempo_total = random.randint(900, 1500)
    enterprise_loc = ()
    total_energy = random.randint(2500, 3000)

    def __init__(self):
        self.mapa = []
        self.estado = {
            "remaining_energy": self.total_energy,
            "remaining_days": self.tiempo_total,
            "remaining_klingons": self.cant_klingon_total,
            "remaining_torpedoes": self.cant_torpedoes,
            "subs_torpedoes": 1,
            "subs_phasers": 1,
            "subs_warp": 1,
            "subs_impulse": 1,
            "subs_shields": 1,
        }
        enterprise = False
        while len(self.mapa) < 8:
            cx = []
            while len(cx) < 8:
                cy = []
                while len(cy) < 8:
                    ox = []
                    while len(ox) < 8:
                        objeto = "---"
                        ox.append(objeto)
                    cy.append(ox)
                cx.append(cy)
            self.mapa.append(cx)

        for _ in range(random.randint(10, 20)):
            r_cx = random.choice(self.mapa)
            r_cy = random.choice(r_cx)
            r_ox = random.choice(r_cy)
            num_random = random.randint(0, 7)
            if r_ox[num_random] == "---":
                r_ox[num_random] = "klingon"

        for _ in range(random.randint(50, 60)):
            r_cx = random.choice(self.mapa)
            r_cy = random.choice(r_cx)
            r_ox = random.choice(r_cy)
            num_random = random.randint(0, 7)
            if r_ox[num_random] == "---":
                r_ox[num_random] = "star"

        for _ in range(random.randint(3, 5)):
            r_cx = random.choice(self.mapa)
            r_cy = random.choice(r_cx)
            r_ox = random.choice(r_cy)
            num_random = random.randint(0, 7)
            if r_ox[num_random] == "---":
                r_ox[num_random] = "starbase"

        while not enterprise:
            print("while")
            r_cx_num = random.randint(0, 7)
            r_cx = self.mapa[r_cx_num]
            r_cy_num = random.randint(0, 7)
            r_cy = r_cx[r_cy_num]
            r_ox_num = random.randint(0, 7)
            r_ox = r_cy[r_ox_num]
            num_random = random.randint(0, 7)
            if r_ox[num_random] == "---":
                r_ox[num_random] = "enterprise"
                self.enterprise_loc = ((r_cx_num, r_cy_num), (r_ox_num, num_random))
                print("enterprise True")
                enterprise = True

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
        self.estado["remaining_energy"] = self.estado["remaining_energy"] - 1

    async def command(self, command):
        if command == "galaxy":
            await self.cmd_galaxy()
        if command == "srs":
            await self.cmd_srs()

    async def cmd_galaxy(self):
        print(self.mapa)

    async def cmd_srs(self):
        cuadrante = self.enterprise_loc[0]
        cuadrante_x = cuadrante[0]
        cuadrante_y = cuadrante[1]
        print(self.mapa[cuadrante_x][cuadrante_y])

    async def cmd_lrs(self):
        x, y= self.enterprise_loc[0]
        for cx in (-1, 0, +1):
            for cy in (-1, 0, +1):
                cant_klingon = 0
                cant_stars = 0
                cant_starbases = 0
                for cuadrante in self.mapa[x - cx][x - cy]:
                    for objeto in cuadrante:
                        if objeto == "klingon":
                            cant_klingon += 1
                        elif objeto == "star":
                            cant_stars += 1
                        elif objeto == "starbase":
                            cant_starbases += 1
                        print(cant_klingon, cant_stars, cant_starbases)

    async def get_state(self):
        return self.estado
