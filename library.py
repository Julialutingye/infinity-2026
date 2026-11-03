from pybricks.tools import multitask, run_task, wait

from robot_config import ACCELERATION, DRIVE_BASE, HUB, SPEED, TURN_ACCELERATION, TURN_SPEED

def set_drivebase(
    *,
    straight_speed=SPEED,
    straight_acceleration=ACCELERATION,
    turn_rate=TURN_SPEED,
    turn_acceleration=TURN_ACCELERATION,
):
    """Apply project defaults with optional overrides for this call."""
    DRIVE_BASE.settings(
        straight_speed=straight_speed,
        straight_acceleration=straight_acceleration,
        turn_rate=turn_rate,
        turn_acceleration=turn_acceleration,
    )

async def print_drivebase_settings():
    print('Default drivebase settings that are overridden in the config file')
    print('Speed, Acceleration, Turn, Turn Accel')
    print(DRIVE_BASE.settings())


async def main():
    # Blank,  done to make code multitask
    # Needed due to how the blocks work
    await multitask(
        wait(0),
    )


run_task(main())