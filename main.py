import pygame
from typing import List

from building_simulation import BuildingSimulation


def main() -> None:
    """
    Initializes Pygame and runs the building simulation.

    This function initializes Pygame and the sound mixer, creates a list of building information,
    creates an instance of BuildingSimulation, and runs the simulation.
    """
    pygame.init()
    pygame.mixer.init()

    buildings_info: List[List[int]] = [
        [15, 3],
        [10, 2],
        [20, 4]
    ]

    simulation = BuildingSimulation(buildings_info, 900, 1700)
    simulation.run()

if __name__ == "__main__":
    main()
