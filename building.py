import pygame
from typing import List, Tuple

class Building:
    """
    Represents a building with multiple floors and elevators.

    Attributes:
        num_floors (int): Number of floors in the building.
        floor_width (float): Width of each floor.
        floor_height (float): Height of each floor.
        elevators (List[Elevator]): List of elevators in the building.
        floors (List[Floor]): List of floors in the building.
        last_time (float): Time of the last frame in seconds.
    """

    def __init__(self, position: float, num_floors: int, num_elevators: int, 
                 floor_width: float, floor_height: float, height_screen: int) -> None:
        """
        Initializes the Building object.

        Args:
            position (float): X position of the building.
            num_floors (int): Number of floors in the building.
            num_elevators (int): Number of elevators in the building.
            floor_width (float): Width of each floor.
            floor_height (float): Height of each floor.
            height_screen (int): Height of the screen in pixels.
        """
        from factory import factory

        self.last_time = pygame.time.get_ticks() / 1000
        self.num_floors = num_floors
        self.floor_width = floor_width
        self.floor_height = floor_height

        self.elevators = [
            factory("elevator", i, floor_height, floor_width / 2, height_screen, floor_width * (i / 2 + 1) + position)
            for i in range(num_elevators)
        ]
        self.floors = [
            factory("floor", i, position, height_screen - (i + 1) * floor_height, floor_width, floor_height)
            for i in range(num_floors + 1)
        ]

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the floors and elevators on the provided surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
            
        Returns:
            None
        """
        for floor in self.floors:
            floor.draw(surface)
        for elv in self.elevators:
            elv.draw(surface)

    def handle_events(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Handles mouse click events and assigns the nearest elevator to the clicked floor.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse click.
            
        Returns:
            None
        """
        for floor in self.floors:
            if floor.handle_events(mouse_pos) == floor.number:
                min_time = float('inf')
                min_elv = None
                for elv in self.elevators:
                    if elv.target_floor == floor.number:
                        return
                    time_elv = elv.calculate_time(floor.number)
                    if time_elv < min_time:
                        min_time = time_elv
                        min_elv = elv

                if min_elv is not None:
                    min_elv.add_to_queue(floor.number)
                    floor.increment_timer(min_time)
                return

    def process_elevator_movement(self) -> None:
        """
        Process the movement of elevators and update floor timers.

        This method iterates through all elevators, calculates their movements,
        and updates the timers for each floor. It also updates the last recorded time.

        Returns:
            None
        """
        current_time = pygame.time.get_ticks() / 1000
        for elv in self.elevators:
            target_floor = elv.target_floor
            height_floor = self.floors[target_floor].get_rect().top
            elv.process_movement(height_floor, current_time, self.last_time)
        for floor in self.floors:
            floor.timer(current_time, self.last_time)
        self.last_time = current_time
