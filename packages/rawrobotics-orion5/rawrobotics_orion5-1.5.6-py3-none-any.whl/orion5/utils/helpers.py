import datetime as dt

DEBUG = False
DEBUG_MODE = 'PRINT'

SERIAL_BAUD_RATE = 1000000
SERIAL_TIMEOUT = 1  # seconds
SERIAL_SLEEP = 0.01  # seconds
SERIAL_MAX_PACKETS_PROCESSED = 5
SERIAL_HEADER_LEN = 4
SERIAL_USB_HEADER = [98, 111, 114, 107]

SOCKET_HOST = 'localhost'
SOCKET_PORT = 41000
SOCKET_MAX_TIMEOUTS = 5

CLAW_OPEN_POS = 300
CLAW_CLOSE_POS = 120

class ErrorIDs:
    INSTRUCTION_ERROR = 0x40
    OVERLOAD_ERROR = 0x20
    CHECKSUM_ERROR = 0x10
    RANGE_ERROR = 0x08
    OVERHEATING_ERROR = 0x04
    ANGLE_LIMIT_ERROR = 0x02
    INPUT_VOLTAGE_ERROR = 0x01

class ControlModes:
    SPEED, TIME, WHEEL = range(3)

class JointVars:
    CURRENT_POS, CURRENT_SPEED, CURRENT_LOAD, GOAL_POS, SPEED, \
        TORQUE_ENABLE, CW_SLOPE, CCW_SLOPE, CW_MARGIN, CCW_MARGIN, \
        PUNCH, CW_LIMIT, CCW_LIMIT, LED, MAX_TORQUE, MODE = range(16)

class GlobalConstants:
    BASE_OFFSET, SHOULDER_OFFSET, ELBOW_OFFSET, WRIST_OFFSET, CLAW_OFFSET, \
    BASE_DIRECTION, SHOULDER_DIRECTION, ELBOW_DIRECTION, WRIST_DIRECTION, \
    CLAW_DIRECTION, CLAW_LOAD_LIMIT, FIELD_INFLATION, CLAW_HOME_POS, FIRMWARE_UPDATE, MODE, ESTOP = range(16)

def getErrorName(code):
    if code == ErrorIDs.INSTRUCTION_ERROR:
        return 'INSTRUCTION_ERROR'
    elif code == ErrorIDs.OVERLOAD_ERROR:
        return 'OVERLOAD_ERROR'
    elif code == ErrorIDs.CHECKSUM_ERROR:
        return 'CHECKSUM_ERROR'
    elif code == ErrorIDs.RANGE_ERROR:
        return 'RANGE_ERROR'
    elif code == ErrorIDs.OVERHEATING_ERROR:
        return 'OVERHEATING_ERROR'
    elif code == ErrorIDs.ANGLE_LIMIT_ERROR:
        return 'ANGLE_LIMIT_ERROR'
    elif code == ErrorIDs.INPUT_VOLTAGE_ERROR:
        return 'INPUT_VOLTAGE_ERROR'

def debug(message):
    if DEBUG:
        timestamp = dt.datetime.now().strftime("%x-%X: ")
        if DEBUG_MODE == "FILE":
            with open('log.txt', 'a') as log:
                log.write(timestamp + message + "\n")
        elif DEBUG_MODE == "PRINT":
            print(timestamp + message)
