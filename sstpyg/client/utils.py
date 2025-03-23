def srs_to_positions(positions):
    k_positions = []
    e_positions = []
    s_positions = []
    b_positions = []

    for i in range(1, 9):
        for j in range(1, 9):
            content = positions[i - 1][j - 1]
            match content:
                case "K":
                    k_positions.append((j, i))
                case "S":
                    s_positions.append((j, i))
                case "B":
                    b_positions.append((j, i))
                case "E":
                    e_positions.append((j, i))

    return k_positions, e_positions, s_positions, b_positions


if __name__ == "__main__":
    positions = [
        ["K", "S", "B", "E", "", "", "", ""],
        ["K", "S", "B", "E", "", "", "", ""],
        ["K", "S", "B", "E", "", "", "", ""],
        ["K", "S", "B", "E", "", "", "", ""],
        ["K", "S", "B", "E", "", "", "", ""],
        ["K", "S", "B", "E", "", "", "", ""],
        ["K", "S", "B", "E", "", "", "", ""],
        ["K", "S", "B", "E", "", "", "", ""],
    ]

    print(srs_to_positions(positions))
