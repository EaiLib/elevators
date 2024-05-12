import pygame
import queue
from enum import Enum

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    PLACE = "place"

class Elevator:
    def __init__(self, number, height, width, height_screen, x):
        self.image = pygame.image.load("elv.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.ring = pygame.mixer.music.load("ding.mp3")
        self.number = number
        self.floor = 0
        self.location = (x, height_screen - self.image.get_rect().height)
        self.target_floor = 0
        self.floor_height = height
        self.elevator_speed = 0.5  # Floors per second
        self.time_elapsed = 0
        self.stay_time = 0
        self.queue = queue.Queue()
        self.last_floor = 0
        self.travel_direction = Direction.PLACE
        self.stay = False

    def draw(self, surface):
        surface.blit(self.image, self.location)

    def update_position(self, current_time, last_time, height_floor):
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

    def adjust_stay_time(self, current_time, last_time):
        self.stay_time += current_time - last_time
        if self.stay_time >= 2:
            self.stay = False
            self.stay_time = 0

    def process_movement(self, height_floor, current_time, last_time):
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

    def add_to_queue(self, number):
        self.queue.put(number)
        time_to_add = abs(number - self.last_floor) * self.elevator_speed + 2
        self.last_floor = number
        self.add_time(time_to_add)

    def add_time(self, number):
        self.time_elapsed += number

    def calculate_time(self, floor):
        return self.time_elapsed + abs(floor - self.last_floor) / 2
