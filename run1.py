from pybricks.parameters import Color, Direction, Stop
from pybricks.tools import multitask, run_task, wait
from library import set_drivebase

from robot_config import DRIVE_BASE, HUB, LEFT_CENTER_ATTACHMENT,FRONT_ATTACHMENT

DRIVE_BASE.settings(straight_speed=700, straight_acceleration=700)

#use this function as a template to define how to drive the base
#drive_base_to_heavy_lifting
async def run1():
    DRIVE_BASE.use_gyro(True) 
    await 
    

if __name__ == "__main__":
    run_task(run1())