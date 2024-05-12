import pygame
from factory import factory

class BuildingSimulation:
    """
    Class representing a simulation of multiple buildings with elevators.

    This class manages the simulation of multiple buildings with elevators. It initializes
    the buildings based on the provided information, handles drawing the buildings on the
    screen, processing elevator movement, and handling user events.

    Attributes:
        buildings (list): A list of buildings in the simulation.

    Methods:
        __init__: Initializes the BuildingSimulation object.
        draw: Draws the buildings on the screen.
        handle_events: Handles user events such as mouse clicks.
        run: Runs the simulation loop.
    """

    def __init__(self, buildings_info: list[list[int]], height_screen: int, width_screen: int) -> None:
        """
        Initializes the BuildingSimulation object.

        This method initializes the BuildingSimulation object by creating buildings
        based on the provided information and storing them in a list.

        Args:
            buildings_info (list[list[int]]): A list of lists containing building information.
                Each inner list contains the number of floors and elevators for a building.
            height_screen (int): The height of the screen in pixels.
            width_screen (int): The width of the screen in pixels.

        Returns:
            None
        """
        self.buildings = []
        sum_buildings = 0
        max_floor = 0
        for building_info in buildings_info:
            sum_buildings += building_info[1] / 2 + 1
            if building_info[0] > max_floor:
                max_floor = building_info[0]
        max_floor += 1
        count = 0
        for building_info in buildings_info:
            position = width_screen / sum_buildings * count + 10
            building = factory("building", position, building_info[0], building_info[1],
                               (width_screen - 20) / sum_buildings, (height_screen - 10) / max_floor, height_screen)
            self.buildings.append(building)
            count += building_info[1] / 2 + 1

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the buildings on the screen.

        This method draws each building in the simulation on the provided surface.

        Args:
            surface (pygame.Surface): The surface to draw the buildings on.

        Returns:
            None
        """
        for building in self.buildings:
            building.draw(surface)
            building.process_elevator_movement()

    def handle_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles user events such as mouse clicks.

        This method processes user events, specifically mouse clicks, and delegates
        the handling to each building in the simulation.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.

        Returns:
            None
        """
        for building in self.buildings:
            building.handle_events(mouse_pos)

    def run(self) -> None:
        """
        Runs the simulation loop.

        This method runs the main simulation loop, handling events, updating the screen,
        and managing the clock for frame rate control.

        Args:
            None

        Returns:
            None
        """
        height_screen = 900
        width_screen = 1700

        pygame.init()
        screen = pygame.display.set_mode((width_screen, height_screen))
        pygame.display.set_caption("Building Floors")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_events(pygame.mouse.get_pos())

            screen.fill((255, 255, 255))  # Fill the screen with white
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
