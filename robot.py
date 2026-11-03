from pybricks.parameters import Color
from pybricks.tools import multitask, run_task, wait

from library import set_drivebase, print_drivebase_settings
from ui import add_program, user_interface

# 2026 missions: M1_Name.py, M2_Name.py; combined runs: M1_M2.py.
from M1_DroneSurvey import main as run_m1

async def main():
    # Import from xbox_teleop the teleop function if you want to use
    # the telop mode and add the telop program
    
    # Blank,  done to make code multitask
    # Needed due to how the blocks work
    await multitask(
        wait(0),
    )
    # Print to consule the default drivebase settings
    await print_drivebase_settings()
    # Override these settings. Note pybricks is conservative with speeds.
    # The default speeds are about 40% of what the motors can handle
    # You probably can double the default speeds in the robot_config file.
    # Conversely the accelration values pybricks creates tend to be too high
    # If your wheels slip your distances will be off. Lower accelration as needed
    # in the robot_config file to eliminate wheel slipage. These values will depend on wheel choice, center of gravity of your robot and robot weight.
    set_drivebase()
    # Add the programs (Missons) below they will appear in the order placed
    # Missions will need to be imported, see example missions/utility programs
    # below
    await add_program(run_m1, '1', Color.GREEN)

    # Launch the user interface
    await user_interface()


if __name__ == "__main__":
    run_task(main())