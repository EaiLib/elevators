import unittest
import pygame
from floor import Floor

class TestFloor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_floor_initialization(self):
        floor = Floor(number=1, x=100, y=100, width=200, height=20)
        self.assertEqual(floor.number, 1)
        self.assertEqual(floor.rect.x, 100)
        self.assertEqual(floor.rect.y, 100)
        self.assertEqual(floor.rect.width, 200)
        self.assertEqual(floor.rect.height, 20)
        self.assertEqual(floor.color, (192, 192, 192))
        self.assertEqual(floor.brick_color, (255, 0, 0))
        self.assertEqual(floor.black_line_color, (0, 0, 0))
        self.assertEqual(floor.height_black_line, 4)
        self.assertIsNotNone(floor.font)
        self.assertEqual(floor.number_color, (0, 0, 0))
        self.assertEqual(floor.time, 0)

    def test_draw_floor_on_screen(self):
        surface = pygame.Surface((800, 600))
        floor = Floor(number=1, x=100, y=100, width=200, height=20)
        floor.draw_floor_on_screen(surface)
        # Add your assertions here based on the expected outcome

if __name__ == '__main__':
    unittest.main()
