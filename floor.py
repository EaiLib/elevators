import pygame



class Floor:
    def __init__(self, number, x, y, width, height):
        self.number = number
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (192, 192, 192)
        self.brick_color = (255, 0, 0)
        self.black_line_color = (0, 0, 0)
        self.height_black_line = 4
        self.font = pygame.font.SysFont(None, 24)
        self.number_color = (0, 0, 0)
        self.time = 0

    def draw(self, surface):
        self.draw_bricks(surface)
        self.draw_black_line(surface)
        self.draw_number(surface)
        if self.time > 0:
            self.draw_timer(surface)

    def draw_bricks(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        brick_width = 4
        brick_height = 2
        spacing = 1
        i = 0
        for row in range(0, self.rect.height - brick_height, brick_height + spacing):
            # Adjust col start based on the row index to create a staggered brick pattern
            col_start = int(brick_width / 2) if i % 2 == 0 else 0
            for col in range(col_start, self.rect.width - brick_width, brick_width + spacing):
                brick_rect = pygame.Rect(self.rect.left + col, self.rect.top + row, brick_width, brick_height)
                pygame.draw.rect(surface, self.brick_color, brick_rect)
            i += 1

    def draw_black_line(self, surface):
        line_rect = pygame.Rect(self.rect.left, self.rect.bottom - self.height_black_line, 
                                self.rect.width, self.height_black_line)
        pygame.draw.rect(surface, self.black_line_color, line_rect)

    def draw_number(self, surface):
        # Calculate position and color settings
        number_rect_width, number_rect_height = 20, 16
        number_rect_position, self.number_color = self.calculate_number_position(number_rect_width, number_rect_height)

        # Draw the background rectangle for the number
        pygame.draw.rect(surface, (192, 192, 192), number_rect_position)
        
        # Render the number text and blit to the surface
        number_text = self.font.render(str(self.number), True, self.number_color)
        text_rect = number_text.get_rect(center=number_rect_position.center)
        surface.blit(number_text, text_rect)

    def calculate_number_position(self, width, height):
        # Determine color and position based on the timer state
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
    
    def draw_timer(self, surface):
        timer_text = self.font.render(f"{self.time:.1f}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(self.rect.left + 20, self.rect.centery))
        surface.blit(timer_text, timer_rect)

    def handle_events(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.time <= 0:
            return self.number
        return -1

    def get_rect(self):
        return self.rect

    def timer(self, current_time, last_time):
        if self.time > 0:
            self.time -= current_time-last_time
        else:
            self.time = 0

    def increment_timer(self, time_to_add):
        if self.time < 0:
            self.time = time_to_add
        else:
            self.time += time_to_add