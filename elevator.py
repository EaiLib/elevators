import pygame
import queue
from enum import Enum

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    PLACE = "place"

class Elevator:
    """Class representing an elevator in the simulation.
    Attributes:
        image (pygame.Surface): The image representing the elevator.
        ring (int): The sound effect indicating elevator arrival.
        number (int): The elevator number.
        floor (int): The current floor number of the elevator.
        location (tuple): The coordinates of the elevator's top-left corner.
        target_floor (int): The target floor number of the elevator.
        floor_height (int): The height of each floor.
        elevator_speed (float): The speed of the elevator in floors per second.
        time_elapsed (float): The elapsed time since the last movement.
        stay_time (float): The time the elevator stays idle at a floor.
        queue (queue.Queue): The queue of target floors.
        last_floor (int): The last visited floor number.
        travel_direction (Direction): The current direction of travel.
        stay (bool): Flag indicating whether the elevator is idle.
    """
    
    

    def __init__(self, number: int, height: int, width: int, height_screen: int, x: int):
        """Initialize the Elevator object.

        Args:
            number (int): The elevator number.
            height (int): The height of the elevator.
            width (int): The width of the elevator.
            height_screen (int): The height of the screen.
            x (int): The x-coordinate of the elevator.

        Returns:
            None
        """
        self.image = pygame.image.load("elv.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.ring = pygame.mixer.music.load("ding.mp3")
        self.number = number
        self.floor = 0
        self.location = (x, height_screen - self.image.get_rect().height)
        self.target_floor = 0
        self.floor_height = height
        self.elevator_speed = 0.5 
        self.time_elapsed = 0
        self.stay_time = 0
        self.queue = queue.Queue()
        self.last_floor = 0
        self.travel_direction = Direction.PLACE
        self.stay = False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the elevator on the screen.

        Args:
            surface (pygame.Surface): The surface to draw the elevator on.

        Returns:
            None
        """
        surface.blit(self.image, self.location)

    def update_position(self, current_time: float, last_time: float, height_floor: int) -> int:
        """Update the position of the elevator.

        Args:
            current_time (float): The current time.
            last_time (float): The time of the last update.
            height_floor (int): The height of the target floor.

        Returns:
            int: Indicates whether the elevator has reached the target floor (1) or not (0).
        """
        distance_to_move = (current_time - last_time) * self.floor_height / self.elevator_speed
        if self.travel_direction == Direction.UP and self.location[1] > height_floor:
            self.location = (self.location[0], self.location[1] - distance_to_move)
        elif self.travel_direction == Direction.DOWN and self.location[1] < height_floor:
            self.location = (self.location[0], self.location[1] + distance_to_move)
        else:
            self.travel_direction = Direction.PLACE
            self.stay = True
            return 1
        return 0

    def adjust_stay_time(self, current_time: float, last_time: float) -> None:
        """Adjust the stay time of the elevator.

        Args:
            current_time (float): The current time.
            last_time (float): The time of the last update.

        Returns:
            None
        """
        self.stay_time += current_time - last_time
        if self.stay_time >= 2:
            self.stay = False
            self.stay_time = 0

    def process_movement(self, height_floor: int, current_time: float, last_time: float) -> int:
        """Process the movement of the elevator.

        Args:
            height_floor (int): The height of the target floor.
            current_time (float): The current time.
            last_time (float): The time of the last update.

        Returns:
            int: Indicates whether the elevator has reached the target floor (-1 for no target floor, 0 for in motion, 1 for reached).
        """
        if self.time_elapsed > 0:
            self.add_time(last_time - current_time)
        else:
            self.time_elapsed = 0
        if self.stay:
            self.adjust_stay_time(current_time, last_time)
        elif self.travel_direction != Direction.PLACE:
            if self.update_position(current_time, last_time, height_floor):
                pygame.mixer.music.play()
                return self.target_floor
        elif not self.queue.empty():
            self.floor = self.target_floor
            self.target_floor = self.queue.get()
            if self.floor < self.target_floor:
                self.travel_direction = Direction.UP
            else:
                self.travel_direction = Direction.DOWN
        return -1

    def add_to_queue(self, number: int) -> None:
        """Add a floor to the elevator's queue.

        Args:
            number (int): The target floor number.

        Returns:
            None
        """
        self.queue.put(number)
        time_to_add = abs(number - self.last_floor) * self.elevator_speed + 2
        self.last_floor = number
        self.add_time(time_to_add)

    def add_time(self, number: float) -> None:
        """Add time to the elevator's elapsed time.

        Args:
            number (float): The time to add.

        Returns:
            None
        """
        self.time_elapsed += number

    def calculate_time(self, floor: int) -> float:
        """Calculate the time needed to reach a certain floor.

        Args:
            floor (int): The target floor number.

        Returns:
            float: The calculated time.
        """
        return self.time_elapsed + abs(floor - self.last_floor) / 2
