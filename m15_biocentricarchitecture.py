from pybricks.parameters import Color, Direction, Stop
from pybricks.tools import multitask, run_task, wait
from robot_config import RIGHT_ATTACHMENT, DRIVE_BASE, HUB, LEFT_ATTACHMENT


async def run2():
    LEFT_ATTACHMENT.reconfigure(Direction.CLOCKWISE,gears=[12,36])
    RIGHT_ATTACHMENT.reconfigure(Direction.CLOCKWISE,gears=[12,36])
    DRIVE_BASE.settings(straight_speed=600, straight_acceleration=600)
    DRIVE_BASE.use_gyro(True)
    await wait(300)

    
    await DRIVE_BASE.straight(-667)
    await DRIVE_BASE.turn(43)
    await RIGHT_ATTACHMENT.run_angle(100, -10)
    await DRIVE_BASE.straight(-135)
    await RIGHT_ATTACHMENT.run_angle(100, 15)
    #await DRIVE_BASE.straight(10)
    await RIGHT_ATTACHMENT.run_angle(70, -56) 
    #await wait(400)
    #await DRIVE_BASE.straight(90)
    #await DRIVE_BASE.turn(-43)
    #await DRIVE_BASE.straight(700)
    #await wait(300)

    DRIVE_BASE.use_gyro(False) 


if __name__ == "__main__":
    run_task(run2())
