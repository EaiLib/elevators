import pygame
from typing import List, Tuple
import logging

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
            factory("elevator", elevator_index, floor_height, floor_width / 2, height_screen, floor_width * (elevator_index / 2 + 1) + position)
            for elevator_index in range(num_elevators)
        ]
        self.floors = [
            factory("floor", floor_number, position, height_screen - (floor_number + 1) * floor_height, floor_width, floor_height)
            for floor_number in range(num_floors + 1)
        ]

    def draw_floors_and_elevators(self, surface: pygame.Surface) -> None:
        """
        Draws the floors and elevators on the provided surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
            
        Returns:
            None
        """
        for floor in self.floors:
            floor.draw_floor_on_screen(surface)
        for elevator in self.elevators:
            elevator.draw_elevator_on_the_screen(surface)

    def assign_and_dispatch_nearest_elevator(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Handles mouse click events and assigns the nearest elevator to the clicked floor.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse click.
            
        Returns:
            None
        """
        logging.info(f"Mouse clicked at position {mouse_pos}")
        for floor in self.floors:
            if floor.handle_events_on_floor(mouse_pos) == floor.number:
                logging.info(f"Floor {floor.number} clicked")
                minimum_time_approach = float('inf')
                nearest_elevator = None
                for elevator in self.elevators:
                    if elevator.target_floor == floor.number:
                        return
                    time_elevator = elevator.calculate_time_for_a_certain_floor(floor.number)
                    if time_elevator < minimum_time_approach:
                        minimum_time_approach = time_elevator
                        nearest_elevator = elevator

                if nearest_elevator is not None:
                    logging.info(f"Dispatching elevator {nearest_elevator.number} to floor {floor.number}")
                    nearest_elevator.add_elevator_to_queue(floor.number)
                    floor.increment_timer(minimum_time_approach)
                return

    def process_elevator_movement(self) -> None:
        """
        Process the movement of elevators and update floor timers.

        This method iterates through all elevators, calculates their movements,
        and updates the timers for each floor. It also updates the last recorded time.

        Returns:
            None
        """
        running_program_time = pygame.time.get_ticks() / 1000
        self.update_elevator_movement(running_program_time)
        self.update_floor_timers(running_program_time)
        self.last_time = running_program_time

    def update_elevator_movement(self, current_time: float) -> None:
        """
        Update elevator movement.

        This method iterates through all elevators, calculates their movements,
        and updates the elevators' positions.

        Args:
            current_time (float): The current time in seconds.

        Returns:
            None
        """
        for elevator in self.elevators:
            target_floor = elevator.target_floor
            height_floor = self.floors[target_floor].get_rect().top
            elevator.process_elevator_movement(height_floor, current_time, self.last_time)

    def update_floor_timers(self, current_time: float) -> None:
        """
        Update floor timers.

        This method iterates through all floors and updates their timers.

        Args:
            current_time (float): The current time in seconds.

        Returns:
            None
        """
        for floor in self.floors:
            floor.timer(current_time, self.last_time)
