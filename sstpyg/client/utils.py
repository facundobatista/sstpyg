def abs_coords_to_sector_coords(abs_coords):
    return (
        ((abs_coords[0] - 1) % 8) + 1,
        ((abs_coords[1] - 1) % 8) + 1,
    )


if __name__ == "__main__":
    print(abs_coords_to_sector_coords((1, 9)))
