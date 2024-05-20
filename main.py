import logging
import os
import pygame
from typing import List

from building_simulation import BuildingSimulation

# Configure logging
log_filename = 'elevator_simulation.log'
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    """
    Initializes Pygame and runs the building simulation.
    
    This function initializes Pygame and the sound mixer, creates a list of building information,
    creates an instance of BuildingSimulation, and runs the simulation.
    """
    logging.info('Starting elevator simulation program')
    
    try:
        pygame.init()
        pygame.mixer.init()

        buildings_info: List[List[int]] = [
            [15, 3],
            [9, 2],
            [20, 5]
        ]

        simulation = BuildingSimulation(buildings_info, 900, 1700)
        simulation.run()
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info('Elevator simulation program ended')

        # Prompt user to delete log file
        delete_log = input(f"Do you want to delete the log file '{log_filename}'? (y/n): ")
        if delete_log.lower() == 'y':
            try:
                os.remove(log_filename)
                print(f"Log file '{log_filename}' deleted.")
            except Exception as e:
                logging.error(f"Failed to delete log file: {e}")
                print(f"Failed to delete log file: {e}")
        else:
            print(f"Log file '{log_filename}' retained.")

if __name__ == "__main__":
    main()
