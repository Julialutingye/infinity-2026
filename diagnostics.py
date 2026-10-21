"""
Robot diagnostics. Checks the hub, battery, gyro, every port, motors and
color sensors, then prints a summary of any problems.

Run it with F5. Output appears in the VS Code terminal.
This file does not import robot_config, because robot_config crashes if a
device is unplugged. Instead it reads the connected hub's name and loads the
matching profile from robot_profiles.py (as robot_config.py does) to decide
what should be plugged into each port.
"""

from pybricks import version
from pybricks.hubs import PrimeHub
from pybricks.iodevices import PUPDevice
from pybricks.parameters import Button, Color, Port
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.tools import wait

from robot_profiles import DEFAULT_PROFILE, PROFILES

ALL_PORTS = (Port.A, Port.B, Port.C, Port.D, Port.E, Port.F)

# Pick the profile for the connected hub, the same way robot_config.py does.
HUB_NAME = PrimeHub().system.name()
if HUB_NAME in PROFILES:
    PROFILE_NAME = HUB_NAME
else:
    PROFILE_NAME = DEFAULT_PROFILE
PROFILE = PROFILES[PROFILE_NAME]


def build_expected(profile):
    """Builds {port: (name, kind, direction)} from a robot_profiles entry.
    Ports the profile doesn't use are (None, None, None)."""
    expected = {port: (None, None, None) for port in ALL_PORTS}
    for key, name in (("drive_left", "DRIVE_LEFT"), ("drive_right", "DRIVE_RIGHT"),
                      ("left_attachment", "LEFT_ATTACHMENT"),
                      ("right_attachment", "RIGHT_ATTACHMENT")):
        config = profile.get(key)
        if config:
            expected[config["port"]] = (name, "motor", config["direction"])
    for key, name in (("left_color_sensor", "LEFT_COLOR_SENSOR"),
                      ("right_color_sensor", "RIGHT_COLOR_SENSOR")):
        port = profile.get(key)
        if port:
            expected[port] = (name, "color", None)
    return expected


# What the hub's profile in robot_profiles.py says is plugged into each port
EXPECTED = build_expected(PROFILE)

DEVICE_NAMES = {
    38: "BOOST motor",
    46: "Technic large motor",
    47: "Technic XL motor",
    48: "SPIKE medium motor",
    49: "SPIKE large motor",
    61: "SPIKE color sensor",
    62: "SPIKE distance sensor",
    63: "SPIKE force sensor",
    65: "SPIKE small motor",
    75: "Technic medium angular motor",
    76: "Technic large angular motor",
}
MOTOR_IDS = (38, 46, 47, 48, 49, 65, 75, 76)
COLOR_SENSOR_ID = 61

# The orientation can only be set when the hub is created, so create it again
# now that the profile is known.
HUB = PrimeHub(top_side=PROFILE["hub_top_side"], front_side=PROFILE["hub_front_side"])
PROBLEMS = []


def problem(text):
    PROBLEMS.append(text)
    print("  !! PROBLEM:", text)


def wait_for_right_button():
    """Waits for a press of the RIGHT button (center stays as the stop button)"""
    while Button.RIGHT not in HUB.buttons.pressed():
        wait(10)
    while Button.RIGHT in HUB.buttons.pressed():
        wait(10)


def check_hub():
    print("=== HUB ===")
    print("  Name:", HUB_NAME)
    print("  Pybricks firmware:", version)
    if HUB_NAME in PROFILES:
        print("  Robot profile:", PROFILE_NAME)
    else:
        print("  Robot profile:", PROFILE_NAME, "(default; no profile named", HUB_NAME + ")")
        problem("No profile for hub '" + HUB_NAME + "' in robot_profiles.py. Expected ports below are for "
                + DEFAULT_PROFILE + ".")


def check_battery():
    print("=== BATTERY ===")
    voltage = HUB.battery.voltage()
    current = HUB.battery.current()
    print("  Voltage:", voltage, "mV")
    print("  Current:", current, "mA")
    if voltage < 7200:
        problem("Battery is low (" + str(voltage) + " mV). Charge it.")
    elif voltage < 7800:
        print("  Battery is OK but not full.")
    else:
        print("  Battery is good.")


def check_gyro():
    print("=== GYRO ===")
    print("  Keep the robot still on a flat surface...")
    wait(1000)
    ready = HUB.imu.ready()
    pitch, roll = HUB.imu.tilt()
    print("  Ready:", ready)
    print("  Stationary:", HUB.imu.stationary())
    print("  Heading:", HUB.imu.heading())
    print("  Tilt: pitch", pitch, " roll", roll)
    if not ready:
        problem("Gyro is not ready. Put the robot on a flat surface and keep it still.")
    if abs(pitch) > 5 or abs(roll) > 5:
        problem("Robot is tilted. Check the hub is mounted flat and the robot is on a flat surface.")


def check_ports():
    """Finds what is plugged into each port and compares it to robot_config"""
    print("=== PORTS ===")
    found = {}
    for port in ALL_PORTS:
        name, kind, _ = EXPECTED[port]
        try:
            device_id = PUPDevice(port).info()["id"]
        except OSError:
            device_id = None

        if device_id is None:
            print(" ", port, ": nothing plugged in")
        else:
            print(" ", port, ":", DEVICE_NAMES.get(device_id, "unknown device " + str(device_id)))
        found[port] = device_id

        if kind is None:
            continue  # the profile doesn't use this port
        if device_id is None:
            problem(str(port) + " should have " + name + " but nothing is plugged in (check the cable).")
        elif kind == "motor" and device_id not in MOTOR_IDS:
            problem(str(port) + " should have a motor (" + name + ") but has something else.")
        elif kind == "color" and device_id != COLOR_SENSOR_ID:
            problem(str(port) + " should have a color sensor (" + name + ") but has something else.")
    return found


def check_motors(found):
    print("=== MOTORS ===")
    print("  Motors will spin. Lift the robot so the wheels are off the table,")
    print("  then press the RIGHT button on the hub to continue.")
    HUB.light.blink(Color.ORANGE, [300, 300])
    wait_for_right_button()
    HUB.light.on(Color.WHITE)

    for port, (name, kind, direction) in EXPECTED.items():
        if kind != "motor" or found[port] not in MOTOR_IDS:
            continue
        motor = Motor(port, direction)
        motor.reset_angle(0)
        motor.run_time(300, 600)
        moved = motor.angle()
        motor.run_time(-300, 600)
        motor.stop()
        print(" ", name, "(" + str(port) + ") turned", moved, "degrees (expected about 180)")
        if abs(moved) < 90:
            problem(name + " barely moved. It may be jammed, or the gears are too tight.")
        if name.startswith("DRIVE"):
            print("    Did the", name, "wheel roll FORWARD first? If not, flip its Direction in robot_config.py.")


def check_color_sensors(found):
    print("=== COLOR SENSORS ===")
    for port, (name, kind, _) in EXPECTED.items():
        if kind != "color" or found[port] != COLOR_SENSOR_ID:
            continue
        sensor = ColorSensor(port)
        print(" ", name, "(" + str(port) + ")")
        print("    color:", sensor.color())
        print("    reflection:", sensor.reflection())
        print("    ambient:", sensor.ambient())


def print_summary():
    print("=== SUMMARY ===")
    if PROBLEMS:
        print(" ", len(PROBLEMS), "problem(s) found:")
        for p in PROBLEMS:
            print("   -", p)
        HUB.light.on(Color.RED)
        HUB.display.char("X")
    else:
        print("  Everything passed!")
        HUB.light.on(Color.GREEN)
        HUB.display.char("P")


def diagnostics():
    check_hub()
    check_battery()
    check_gyro()
    found = check_ports()
    check_motors(found)
    check_color_sensors(found)
    print_summary()
    wait(3000)


if __name__ == "__main__":
    diagnostics()
