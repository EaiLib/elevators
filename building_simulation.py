import pygame
from factory import factory
from typing import List, Tuple

class BuildingSimulation:
    """
    Class representing a simulation of multiple buildings with elevators.

    This class manages the simulation of multiple buildings with elevators. It initializes
    the buildings based on the provided information, handles drawing the buildings on the
    screen, processing elevator movement, and handling user events.

    Attributes:
        buildings (List): A list of buildings in the simulation.
        height_screen (int): The height of the screen in pixels.
        width_screen (int): The width of the screen in pixels.
    """

    def __init__(self, buildings_content: List[List[int]], height_screen: int, width_screen: int) -> None:
        """
        Initializes the BuildingSimulation object.

        This method initializes the BuildingSimulation object by creating buildings
        based on the provided information and storing them in a list.

        Args:
            buildings_content (List[List[int]]): A list of lists containing building information.
                Each inner list contains the number of floors and elevators for a building.
            height_screen (int): The height of the screen in pixels.
            width_screen (int): The width of the screen in pixels.
        """
        self.height_screen = height_screen
        self.width_screen = width_screen
        self.buildings = self.create_buildings(buildings_content)

    def create_buildings(self, buildings_content: List[List[int]]) -> List:
        """
        Creates building objects based on the provided information.

        Args:
            buildings_content (List[List[int]]): A list of lists containing building information.

        Returns:
            List: A list of building objects.
        """
        sum_buildings = sum(content[1] / 2 + 1 for content in buildings_content)
        max_floor = max(content[0] for content in buildings_content) + 1

        buildings = []
        count = 0
        for content in buildings_content:
            position = self.width_screen / sum_buildings * count + 10
            building = factory(
                "building",
                position,
                content[0],
                content[1],
                (self.width_screen - 20) / sum_buildings,
                (self.height_screen - 10) / max_floor,
                self.height_screen
            )
            buildings.append(building)
            count += content[1] / 2 + 1
        return buildings

    def render_simulation(self, surface: pygame.Surface) -> None:
        """
        Draws the buildings on the screen.

        This method draws each building in the simulation on the provided surface.

        Args:
            surface (pygame.Surface): The surface to draw the buildings on.
        """
        for building in self.buildings:
            building.draw_floors_and_elevators(surface)
            building.process_elevator_movement()

    def process_simulation_events(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Handles user events such as mouse clicks.

        This method processes user events, specifically mouse clicks, and delegates
        the handling to each building in the simulation.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        for building in self.buildings:
            building.assign_and_dispatch_nearest_elevator(mouse_pos)

    def run(self) -> None:
        """
        Runs the simulation loop.

        This method runs the main simulation loop, handling events, updating the screen,
        and managing the clock for frame rate control.
        """
        pygame.init()
        screen = pygame.display.set_mode((self.width_screen, self.height_screen))
        pygame.display.set_caption("Elevator Challenge")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.process_simulation_events(pygame.mouse.get_pos())

            screen.fill((255, 255, 255))
            self.render_simulation(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
