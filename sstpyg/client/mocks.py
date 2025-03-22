import random
from pprint import pprint


def srs():
    srs_list = []
    row_list = []
    possible_objects = ["K", "S", "", "", "", "", "", "B", "E"]

    for i in range(0, 8):
        for j in range(0, 8):
            choice = random.choice(possible_objects)
            if choice == "E":
                possible_objects.pop()
            row_list.append(choice)
        srs_list.append(row_list)
        row_list = []
    return srs_list


if __name__ == "__main__":
    for row in srs():
        print(row)
