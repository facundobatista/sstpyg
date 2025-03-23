import random
from pprint import pprint

from sstpyg.client.constants import AppState


def get_server_info():
    return {
        AppState.REMAINING_KLINGONS.value: 0,
        AppState.REMAINING_DAYS.value: 10,
        AppState.SHIP_TOTAL_ENERGY.value: 10,
        AppState.SHIP_ENG_ENERGY.value: 10,
        AppState.SHIP_OK.value: True,
        AppState.SUBSYSTEM_TORPEDO.value: 20,
        AppState.SUBSYSTEM_PHASERS.value: 20,
        AppState.SUBSYSTEM_WARP_ENGINE.value: 20,
        AppState.SUBSYSTEM_SHIELD.value: 50,
        AppState.SUBSYSTEM_IMPULSE.value: 80,
        AppState.KLINGON_SHIPS_COORDS.value: [
            (1, 3),
            (6, 6),
            (8, 8),
            (1, 8),
        ],
        AppState.ENTERPRISE_POSITION.value: (1, 1),
        AppState.ENTERPRISE_QUADRANT.value: (1, 1),
    }


def lrs():
    lrs_list = []
    for i in range(0, 3):
        for j in range(0, 3):
            lrs_list.append((111, 222, 333))
    return lrs_list


def srs():
    srs_list = []
    row_list = []
    possible_objects = ["K", "S", "", "", "", "", "", "B", "E"]
    k_objs = 0
    s_objs = 0
    b_objs = 0
    max_obj = 9

    for i in range(0, 8):
        for j in range(0, 8):
            choice = random.choice(possible_objects)
            if choice == "E":
                possible_objects.remove("E")
            if choice == "K":
                k_objs += 1
                if k_objs == max_obj:
                    possible_objects.remove("K")
            if choice == "S":
                s_objs += 1
                if s_objs == max_obj:
                    possible_objects.remove("S")
            if choice == "B":
                b_objs += 1
                if b_objs == max_obj:
                    possible_objects.remove("B")
            row_list.append(choice)
        srs_list.append(row_list)
        row_list = []
    return srs_list


if __name__ == "__main__":
    for row in srs():
        print(row)
