import random
from pprint import pprint


def srs():
    srs_list = []
    row_list = []
    possible_objects = ["K", "S", "", "", "", "", "", "B", "E"]
    k_objs = 0
    s_objs = 0
    b_objs = 0
    e_objs = 0
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
