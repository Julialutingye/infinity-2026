
from pybricks.tools import multitask, run_task, wait
from robot_config import DRIVE_RIGHT, LEFT_ATTACHMENT, RIGHT_ATTACHMENT

from library import set_drivebase
from robot_config import DRIVE_BASE


async def M13():
    await set_drivebase()
    DRIVE_BASE.settings(
        straight_speed=300,
        straight_acceleration=500,
        turn_rate=600,
        turn_acceleration=600,
    )
    DRIVE_BASE.use_gyro(True)
    await DRIVE_BASE.straight(-660)
    await DRIVE_BASE.turn(45)
    await DRIVE_BASE.straight(-300)
    await DRIVE_BASE.curve(-200, 70)
    await DRIVE_BASE.straight(800)
if __name__ == "__main__":
    run_task(M13())