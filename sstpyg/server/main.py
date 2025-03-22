from sstpyg.comms import Communications
import random

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
        cuadrante = []
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
        print("enterprise")
        while len(self.mapa) < 8:
            cx = []
            while len(cx) < 8:
                cy =[]
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

        while enterprise == False:
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
                self.enterprise_loc = ((r_cx_num, r_cy_num),(r_ox_num, num_random))
                print("enterprise True")
                enterprise = True

    def commands(command):
        if coomand == "galaxy":
            cmd_galaxy()
        if command == "srs":
            cmd_srs()

    def cmd_galaxy(self):
        print(self.mapa)

    def cmd_srs(self):
        cuadrante = self.enterprise_loc[0]
        cuadrante_x = cuadrante[0]
        cuadrante_y = cuadrante[1]
        #breakpoint()
        print(self.mapa[cuadrante_x][cuadrante_y])

    def get_state(self):
        return self.estado
