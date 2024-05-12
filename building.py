import pygame

class Building:
    def __init__(self, position, num_floors, num_elevators, floor_width, floor_height, height_screen):        
        from factory import factory
        self.last_time = pygame.time.get_ticks() / 1000 #in second
        self.num_floors = num_floors
        self.floor_width = floor_width
        self.floor_height = floor_height
        self.elevators = []
        for i in range(num_elevators):
            elv = factory("elevator", i, floor_height, floor_width/2 , height_screen, floor_width * (i/2 +1) + position)
            self.elevators.append(elv)
        self.floors = []
        for i in range(num_floors+1):
            floor = factory("floor", i, position, height_screen - (i + 1) * floor_height, floor_width, floor_height)
            self.floors.append(floor)

    def draw(self, surface):
        for floor in self.floors:
            floor.draw(surface)
        for elv in self.elevators:
            elv.draw(surface)

    def handle_events(self, mouse_pos):
        for floor in self.floors:
            check = floor.handle_events(mouse_pos)
            if check == floor.number:
                min_time = float('inf')
                min_elv = 0
                for elv in self.elevators:
                    time_elv = elv.calculate_time(check)
                    if elv.target_floor == check:
                        return
                    if time_elv < min_time:
                        min_time = time_elv
                        min_elv = elv.number

                self.elevators[min_elv].add_to_queue(check)
                self.floors[check].increment_timer(min_time)
                return
                        
    def process_elevator_movement(self):
        current_time = pygame.time.get_ticks() / 1000 #in second
        for elv in self.elevators:
            target_floor = elv.target_floor
            height_floor = self.floors[target_floor].get_rect().top
            floor = elv.process_movement(height_floor, current_time, self.last_time)
        for floor in self.floors:
            floor.timer(current_time, self.last_time)
        self.last_time = current_time
