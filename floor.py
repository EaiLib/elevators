import pygame


class Floor:
    """
    Represents a floor in a building.

    Attributes:
        number (int): The floor number.
        rect (pygame.Rect): The rectangular area representing the floor.
        color (tuple): The color of the floor.
        brick_color (tuple): The color of the bricks on the floor.
        black_line_color (tuple): The color of the black line at the bottom of the floor.
        height_black_line (int): The height of the black line.
        font (pygame.font.Font): The font used for rendering text.
        number_color (tuple): The color of the floor number.
        time (float): The remaining time for an event on the floor.
    """

    def __init__(self, number: int, x: int, y: int, width: int, height: int) -> None:
        """
        Initialize a Floor object.

        Args:
            number (int): The floor number.
            x (int): The x-coordinate of the top-left corner of the floor.
            y (int): The y-coordinate of the top-left corner of the floor.
            width (int): The width of the floor.
            height (int): The height of the floor.

        Returns:
            None
        """
        self.number = number
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (192, 192, 192)
        self.brick_color = (255, 0, 0)
        self.black_line_color = (0, 0, 0)
        self.height_black_line = 4
        self.font = pygame.font.SysFont(None, 24)
        self.number_color = (0, 0, 0)
        self.time = 0

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the floor on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the floor on.

        Returns:
            None
        """
        self._draw_bricks(surface)
        self._draw_black_line(surface)
        self._draw_number(surface)
        if self.time > 0:
            self._draw_timer(surface)

    def _draw_bricks(self, surface: pygame.Surface) -> None:
        """
        Draw the brick pattern on the floor.

        Args:
            surface (pygame.Surface): The surface to draw the brick pattern on.

        Returns:
            None
        """
        pygame.draw.rect(surface, self.color, self.rect)
        brick_width = 4
        brick_height = 2
        spacing = 1
        i = 0
        for row in range(0, self.rect.height - brick_height, brick_height + spacing):
            col_start = int(brick_width / 2) if i % 2 == 0 else 0
            for col in range(col_start, self.rect.width - brick_width, brick_width + spacing):
                brick_rect = pygame.Rect(self.rect.left + col, self.rect.top + row, brick_width, brick_height)
                pygame.draw.rect(surface, self.brick_color, brick_rect)
            i += 1

    def _draw_black_line(self, surface: pygame.Surface) -> None:
        """
        Draw the black line at the bottom of the floor.

        Args:
            surface (pygame.Surface): The surface to draw the black line on.

        Returns:
            None
        """
        line_rect = pygame.Rect(self.rect.left, self.rect.bottom - self.height_black_line,
                                self.rect.width, self.height_black_line)
        pygame.draw.rect(surface, self.black_line_color, line_rect)

    def _draw_number(self, surface: pygame.Surface) -> None:
        """
        Draw the floor number on the floor.

        Args:
            surface (pygame.Surface): The surface to draw the floor number on.

        Returns:
            None
        """
        number_rect_width, number_rect_height = 20, 16
        number_rect_position, self.number_color = self._calculate_number_position(number_rect_width, number_rect_height)
        pygame.draw.rect(surface, (192, 192, 192), number_rect_position)
        number_text = self.font.render(str(self.number), True, self.number_color)
        text_rect = number_text.get_rect(center=number_rect_position.center)
        surface.blit(number_text, text_rect)

    def _calculate_number_position(self, width: int, height: int) -> tuple[pygame.Rect, tuple[int, int, int]]:
        """
        Calculate the position and color settings for the floor number.

        Args:
            width (int): The width of the number rectangle.
            height (int): The height of the number rectangle.

        Returns:
            tuple[pygame.Rect, tuple[int, int, int]]: A tuple containing the position and color settings.
        """
        if self.time > 0:
            color = (0, 255, 0)
            position = pygame.Rect(self.rect.right - width - 10,
                                   self.rect.centery - (height / 2),
                                   width, height)
        else:
            color = (0, 0, 0)
            position = pygame.Rect(self.rect.centerx - (width / 2),
                                   self.rect.centery - (height / 2),
                                   width, height)
        return position, color

    def _draw_timer(self, surface: pygame.Surface) -> None:
        """
        Draw the timer on the floor.

        Args:
            surface (pygame.Surface): The surface to draw the timer on.

        Returns:
            None
        """
        timer_text = self.font.render(f"{self.time:.1f}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(self.rect.left + 20, self.rect.centery))
        surface.blit(timer_text, timer_rect)

    def handle_events(self, mouse_pos: tuple[int, int]) -> int:
        """
        Handle mouse events on the floor.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.

        Returns:
            int: The floor number if clicked, otherwise -1.
        """
        if self.rect.collidepoint(mouse_pos) and self.time <= 0:
            return self.number
        return -1

    def get_rect(self) -> pygame.Rect:
        """
        Get the rectangle representing the floor.

        Returns:
            pygame.Rect: The rectangle representing the floor.
        """
        return self.rect

    def timer(self, current_time: float, last_time: float) -> None:
        """
        Update the timer for the floor.

        Args:
            current_time (float): The current time.
            last_time (float): The time from the last update.

        Returns:
            None
        """
        if self.time > 0:
            self.time -= current_time - last_time
        else:
            self.time = 0

    def increment_timer(self, time_to_add: float) -> None:
        """
        Increment the timer for the floor.

        Args:
            time_to_add (float): The time to add to the floor's timer.

        Returns:
            None
        """
        if self.time < 0:
            self.time = time_to_add
        else:
            self.time += time_to_add
