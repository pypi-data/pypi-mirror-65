import copy
import time, datetime
import threading
import traceback

from . import utils
from . import orion5_math
from . import orion5_serial
from . import orion5_client


# TODO: use functions from orion5_math
DEG_TO_CYTRON_CONVERT = 1088/360


class ServerBusyException(Exception):
    def __init__(self, message):
        self.message = message


def test_server():
    try:
        o5_client = orion5_client.Orion5Client()
        o5_client.connect(timer=False)
        data = o5_client._ping()

    except Exception as e:
        print('test server error:', e)
        traceback.print_tb(e.__traceback__)

    else:
        if data:
            if o5_client._set_flag():
                o5_client._start_ping()
                return o5_client
            else:
                raise ServerBusyException('Could not connect to server, is code running elsewhere?')

        return False


# Single constructor for Orion5 and Orion5Client objects
# available modes: 'auto', 'server' (default), 'standalone'
#     auto: if the server exists and the flag can be set, then return an Orion5Client, otherwise return an Orion5Obj
#     server: same as auto, but return error if connecting to server failed
#     standalone: return an orion5 object with args passsed through
def Orion5(mode='server', *args, **kwargs):
    if mode == 'server' or mode == 'auto':
        result = test_server()
        if result or mode == 'server':
            return result
        else:
            mode = 'standalone'

    if mode == 'standalone':
        return Orion5Obj(*args, **kwargs)



class Joint(object):
    def __init__(self, name, ID, cwAngleLimit, ccwAngleLimit, margin, slope, punch, speed, mode, inverter = 1, pos=0):
        self._jointLock = threading.Lock()
        '''TODO, later make the flag also be the checker,
        too tedious to properly do right now so third
        entry is now the checker'''
        self._datam = {
            'constants': {
                'ID': [ID, 1],
                'name': [name, 1]
            },
            'misc variables': {
                'cwAngleLimit': [cwAngleLimit, 0],
                'ccwAngleLimit': [ccwAngleLimit, 0],
                'cwMargin': [margin, 0],
                'cwwMargin': [margin, 0],
                'cwSlope': [slope, 0],
                'cwwSlope': [slope, 0],
                'punch': [punch, 0],
                'error': [None, 0]
            },
            'control variables': {
                'enable': [0, 1],
                'goalPosition': [pos, 0],
                'desiredSpeed': [speed, 1],
                'controlMode': [mode, 1]
            },
            'feedback variables': {
                'currentPosition': [pos, 0],
                'currentVelocity': [0, 0],
                'currentLoad': [0, 0],
                'moving':[None, 0],
                'approachDist':[None, 0],
                'goalDistance':[None, 0],
                'inverter':[inverter, 0]
            }
        }


    def setVariable(self, id1, id2, datum):
        self._jointLock.acquire()
        if (self._datam['constants']['ID'][0] == 1) and (id1 == 'control variables') and (id2 == 'goalPosition'):
            datum *= orion5_math.SHOULDER_GEAR_RATIO
        self._datam[id1][id2] = [datum, 1]
        self._jointLock.release()
        return


    def getVariable(self, id1, id2):
        self._jointLock.acquire()
        retValue = copy.copy(self._datam[id1][id2][0])
        if (self._datam['constants']['ID'][0] == 1) and (id1 == 'feedback variables') and (id2 == 'currentPosition') and retValue is not None:
            retValue /= orion5_math.SHOULDER_GEAR_RATIO
        self._jointLock.release()
        return retValue


    def setTick(self, id1, id2, Tick):
        self._jointLock.acquire()
        self._datam[id1][id2][1] = Tick
        self._jointLock.release()
        return


    def checkVariable(self, id1, id2):
        self._jointLock.acquire()
        retValue = copy.copy(self._datam[id1][id2][1])
        self._jointLock.release()
        return retValue


    def TickVariable(self, id1, id2):
        self._jointLock.acquire()
        if self._datam[id1][id2][1] == 0:
            self._datam[id1][id2][1] = 1
        else:
            self._datam[id1][id2][1] = 0
        self._jointLock.release()
        return


    # SETTERS
    def setTorqueEnable(self, enable):
        self.setVariable('control variables', 'enable', int(enable))


    def setControlMode(self, mode):
        self.setVariable('control variables', 'controlMode', mode)


    def setPosition(self, goalPosition):
        self.setVariable('control variables', 'goalPosition', goalPosition)


    def setTimeToGoal(self, seconds):
        seconds = int(seconds * 10)
        assert self.getVariable('control variables', 'controlMode') == utils.ControlModes.TIME, "Control mode not set to time"
        assert 0 <= seconds <= 1023, "Time outside valid range: 0-1024"
        self.setVariable('control variables', 'desiredSpeed', seconds)


    def setSpeed(self, RPM):
        assert self.getVariable('control variables', 'controlMode') in [utils.ControlModes.WHEEL, utils.ControlModes.SPEED], "Control mode set to time"
        assert 0 <= RPM <= 100, "RPM value outside valid range: 0-100"
        self.setVariable('control variables', 'desiredSpeed', int(1023.0 * RPM / 112.83))


    # GETTERS
    def getPosition(self):
        retValue = self.getVariable('feedback variables', 'currentPosition')
        if retValue == None:
            retValue = 0.0
        return retValue


    def getSpeed(self):
        retValue = self.getVariable('feedback variables', 'currentVelocity')
        if retValue == None:
            retValue = 0.0
        return retValue


    def getLoad(self):
        retValue = self.getVariable('feedback variables', 'currentLoad')
        if retValue == None:
            retValue = 0.0
        return retValue



class Orion5Obj(object):
    def __init__(self, serialName=None, useSimulator=False):
        self._constantLock = threading.Lock()
        self._functionalVariablesLock = threading.Lock()

        # name, ID, cwAngleLimit, ccwAngleLimit, margin, slope, punch, speed, mode, servo direction, initial pos
        self.base =     Joint('base',     0, 1087,    0,   1,  120,  35,  110,  0, -1,   0.00)
        self.shoulder = Joint('shoulder', 1,   30, 1057,   1,  120,  35,  150,  0, -1, 151.75)
        self.elbow =    Joint('elbow',    2,   60, 1027,   1,  120,  35,   80,  0,  1,  50.53)
        self.wrist =    Joint('wrist',    3,  136,  951,   1,  120,  35,  120,  0, -1, 259.26)
        self.claw =     Joint('claw',     4,   60, 1087,   1,  120,  35,  100,  0,  1, 200.00)

        self.joints = [self.base, self.shoulder, self.elbow, self.wrist, self.claw]

        self.serialName = serialName

        self.simulator = None
        if useSimulator:
            self.simulator = Simulator(self, 0.65)

        self.Simulator = {
            'value': False,
            'new stamp': None,
            'old stamp': None,
            'serialName': serialName,
            'tune': 0.6
        }

        self._globalConstants = {
            'baseOffset':        [0, 0],
            'shoulderOffset':    [0, 0],
            'elbowOffset':       [0, 0],
            'wristOffset':       [0, 0],
            'clawOffset':        [0, 0],
            'baseDirection':     [-1, 0],
            'shoulderDirection': [-1, 0],
            'elbowDirection':    [1, 0],
            'wristDirection':    [-1, 0],
            'clawDirection':     [1, 0],
            'clawLoadLimit':     [500, 1],
            'fieldInflation':    [5, 1],
            'clawHomePos':       [362, 1],
            'firmwareUpdate':    [0, 0],
            'mode':              [0, 0],
            'Estop':             [0, 0],
            'firmwareVersion':   [-1, 0],
            'serialNum':   [-1, 0]
        }

        self._functionalVariables = {
            'SimulatorMode':True,
            'EstopSW':False,
            'Timestamp':0
        }

        self.serial = None
        if self.serialName is not None:
            self.restartSerial('start')


    def setVariable(self, key, value, func = False):
        if func:
            self._functionalVariablesLock.acquire()
            self._functionalVariables[key] = value
            self._functionalVariablesLock.release()
        else:
            self._constantLock.acquire()
            self._globalConstants[key] = [value, 1]
            self._constantLock.release()
        return


    def getVariable(self, key, func = False):
        if func:
            self._functionalVariablesLock.acquire()
            retValue = copy.copy(self._functionalVariables[key])
            self._functionalVariablesLock.release()
        else:
            self._constantLock.acquire()
            retValue = copy.copy(self._globalConstants[key][0])
            self._constantLock.release()
        return retValue


    def setTick(self, key, Tick):
        self._constantLock.acquire()
        self._globalConstants[key][1] = Tick
        self._constantLock.release()
        return


    def checkVariable(self, key):
        self._constantLock.acquire()
        retValue = copy.copy(self._globalConstants[key][1])
        self._constantLock.release()
        return retValue


    def TickVariable(self, key):
        self._constantLock.acquire()
        if self._globalConstants[key][1] == 0:
            self._globalConstants[key][1] = 1
        else:
            self._globalConstants[key][1] = 0
        self._constantLock.release()
        return


    # SETTERS FOR ALL JOINTS
    def setAllJointsPosition(self, angles):
        for i in range(len(angles)):
            self.joints[i].setPosition(angles[i])


    def setAllJointsSpeed(self, speeds):
        for i in range(len(speeds)):
            self.joints[i].setSpeed(speeds[i])


    def setAllJointsTimeToGoal(self, times):
        for i in range(len(times)):
            self.joints[i].setTimeToGoal(times[i])


    def setAllJointsTorqueEnable(self, enables):
        for i in range(len(enables)):
            self.joints[i].setTorqueEnable(enables[i])


    # GETTERS FOR ALL JOINTS
    def getAllJointsPosition(self):
        return [joint.getPosition() for joint in self.joints]


    def getAllJointsSpeed(self):
        return [joint.getSpeed() for joint in self.joints]


    def getAllJointsLoad(self):
        return [joint.getLoad() for joint in self.joints]


    def getAllJointsError(self):
        return [joint.getVariable('misc variables', 'error') for joint in self.joints]

    # ENABLE/DISABLE TORQUE FOR ALL JOINTS
    def releaseTorque(self):
        for joint in self.joints:
            joint.setTorqueEnable(0)


    def enableTorque(self):
        for joint in self.joints:
            joint.setTorqueEnable(1)


    def restartSerial(self, command = 'restart', serialName = None):

        self.setVariable('firmwareVersion', -1)
        self.setVariable('serialNum', -1)

        if serialName != None:
            self.serialName = serialName

        if command == 'restart' or command == 'stop':
            try:
                utils.debug("Orion5: exiting serial thread")
                print(self.serial)
                if self.serial is not None:
                    self.serial.stop()
                    self.serial.join()
                self.serial = None
                utils.debug("Orion5: serial thread exited")
            except Exception as e:
                utils.debug("Orion5: error exiting serial thread?"+str(e))

        if (command == 'restart' or command == 'start') and self.serialName != None:
            try:
                utils.debug("Orion5: restarting serial thread")
                self.serial = orion5_serial.SerialThread(self, self.serialName)
                self.serial.start()
                utils.debug("Orion5: serial thread restarted")
            except Exception as e:
                print("Orion5: error exiting serial thread?\n"+str(e))
                utils.debug("Orion5: error exiting serial thread?"+str(e))


    def checkTicks(self):
        _outboxIterator = [
            [
                'misc variables', [
                    ['cwAngleLimit', utils.JointVars.CW_LIMIT, 2],
                    ['ccwAngleLimit', utils.JointVars.CCW_LIMIT, 2],
                    ['cwMargin', utils.JointVars.CW_MARGIN, 1],
                    ['cwwMargin', utils.JointVars.CCW_MARGIN, 1],
                    ['cwSlope', utils.JointVars.CW_SLOPE, 1],
                    ['cwwSlope', utils.JointVars.CCW_SLOPE, 1],
                    ['punch', utils.JointVars.PUNCH, 2]
                ]
            ],
            [
                'control variables', [
                    ['enable', utils.JointVars.TORQUE_ENABLE, 1],
                    ['goalPosition', utils.JointVars.GOAL_POS, 2],
                    ['desiredSpeed', utils.JointVars.SPEED, 2],
                    ['controlMode', utils.JointVars.MODE, 1]
                ]
            ]
        ]

        _globalConstIterator = [
            ['baseOffset', utils.GlobalConstants.BASE_OFFSET],
            ['shoulderOffset', utils.GlobalConstants.SHOULDER_OFFSET],
            ['elbowOffset', utils.GlobalConstants.ELBOW_OFFSET],
            ['wristOffset', utils.GlobalConstants.WRIST_OFFSET],
            ['clawOffset', utils.GlobalConstants.CLAW_OFFSET],
            ['baseDirection', utils.GlobalConstants.BASE_DIRECTION],
            ['shoulderDirection', utils.GlobalConstants.SHOULDER_DIRECTION],
            ['elbowDirection', utils.GlobalConstants.ELBOW_DIRECTION],
            ['wristDirection', utils.GlobalConstants.WRIST_DIRECTION],
            ['clawDirection', utils.GlobalConstants.CLAW_DIRECTION],
            ['clawLoadLimit', utils.GlobalConstants.CLAW_LOAD_LIMIT],
            ['fieldInflation', utils.GlobalConstants.FIELD_INFLATION],
            ['clawHomePos', utils.GlobalConstants.CLAW_HOME_POS],
            ['firmwareUpdate', utils.GlobalConstants.FIRMWARE_UPDATE],
            ['mode', utils.GlobalConstants.CLAW_HOME_POS],
            ['Estop', utils.GlobalConstants.ESTOP]
        ]

        _outboxIterator2 = []
        for item1 in _outboxIterator:
            #print('item1',type(item1))
            for item2 in item1[1]:
                #print(type(item2))
                for item3 in range(0, 5):
                    _outboxIterator2.append([self.joints[item3], item1[0], item2[0], item2[1], item2[2], item3, True, 0])
        for item in _globalConstIterator:
            item.append(False)
            item.append(0)
            _outboxIterator2.append(item)


        for item in _outboxIterator2:
            if item[-2]:
                if item[0].checkVariable(item[1], item[2]):
                    return False
            else:
                if self.checkVariable(item[0]):
                    return False
        return True

    def exit(self):
        utils.debug("Orion5: exit: joining threads")
        if self.serial is not None:
            self.serial.stop()
            self.serial.join()
        utils.debug("Orion5: exit: finished")



class SimBall(object):
    '''
    This is a ball object, for use by the simulator, these things have the properties
    x,y,z and wether or not they are gripped.

    During an update round, if gripped they will move relative to the tool point.
    otherwise they will 'fall' but not roll or arc, later that might be added but
    it is not important yet, probably this needs to be done with the JS engine to
    do that properly
    '''
    _radius = 20
    def __init__(self, x, y, z, gripped = True, r = 25, theta = 0): #r and theta are for gripped position in a claw
        self._position = {'x':x, 'y':y, 'z':z}
        self._gripped = {'value':gripped, 'r':r, 'theta':theta}



class Simulator(object):
    '''
    This object only comes into existence when needed and is destroyed when not needed.
    The object is created when a visualiser

    Activation involves killing the serial thread, the object already existing,
    initialising some vars, etc.

    Deactivation involves resetting init vars, restarting the serial thread, deleting the object
    '''
    def __init__(self, parent, tuner = 0.5):
        self._stamps = {'new stamp':None, 'old stamp':None, 'time difference':None}
        self.value = False
        self.parent = parent
        self.tuner = tuner
        self.balls = []


    def Start(self):
        if not self.value:
            self.parent.restartSerial('stop')
            self.value = True
            self._stamps['new stamp'] = datetime.datetime.now()

            for item in self.parent.joints:
                #Reset Moving Speed of them all to zero
                item.setVariable('feedback variables', 'currentVelocity', 0)
                item.setVariable('feedback variables', 'moving', 0)
                #Reset any servo loads from run state
                item.setVariable('feedback variables', 'currentLoad', 0)
                #Reset acceleration stuff
                item.setVariable('feedback variables', 'approachDist', 0)
                item.setVariable('feedback variables', 'goalDistance', 0)
                #Set all currentpos to goalpos, in terms of the shoulder this is fine
                item.setVariable('feedback variables', 'currentPosition',
                    item.getVariable('control variables', 'goalPosition'))


    def Stop(self):
        if self.value:
            for item in self.parent.joints:
                #kill all simulator goal position ticks
                item.setTick('control variables', 'goalPosition', 0)

            self._stamps['new stamp'] = None
            self._stamps['old stamp'] = None
            self.parent.restartSerial('start')
            self.value = False


    def ValidateGoals(self):
        for item in self.parent.joints[1:]:
            goalpos = item.getVariable('control variables', 'goalPosition')
            cwlimit = item.getVariable('misc variables', 'cwAngleLimit')
            ccwlimit = item.getVariable('misc variables', 'ccwAngleLimit')
            '''if item == self.parent.shoulder:
                goalpos /= orion5_math.SHOULDER_GEAR_RATIO'''
            if item == self.parent.claw and self.balls != []:
                cwlimit = 500 #Diameter of balls in cytron numbers...   60 to 500 here atm
            goalpos *= DEG_TO_CYTRON_CONVERT
            #print(item.getVariable('constants','ID'), goalpos, cwlimit, ccwlimit)
            if not (goalpos >= cwlimit and goalpos <= ccwlimit):
                centerpos = (cwlimit + ccwlimit)/2
                centerdist = goalpos - centerpos
                if abs(centerdist) > 543:
                    centerdist *= -1
                if centerdist > 0:
                    goalpos = ccwlimit
                else:
                    goalpos = cwlimit
                #print('#####',item.getVariable('constants','ID'), goalpos)
                goalpos /= DEG_TO_CYTRON_CONVERT
                if item == self.parent.shoulder:
                    goalpos /= orion5_math.SHOULDER_GEAR_RATIO
                item.setVariable('control variables', 'goalPosition', goalpos)


    def Update(self):
        if self.value:
            self._stamps['old stamp'] = self._stamps['new stamp']
            self._stamps['new stamp'] = datetime.datetime.now()
            self._stamps['time difference'] = (self._stamps['new stamp'] -
                self._stamps['old stamp']).total_seconds()

        if not self.parent.getVariable('Estop'):
            self.ValidateGoals()
            for item in self.parent.joints:

                goalPos = item.getVariable('control variables', 'goalPosition')
                currentPos = item.getVariable('feedback variables', 'currentPosition')
                desiredSpeed = item.getVariable('control variables', 'desiredSpeed')

                # if shoulder - deappliate gear ratio
                if item is self.parent.shoulder:
                    currentPos *= orion5_math.SHOULDER_GEAR_RATIO

                #Find the direction of travel
                directionVector = orion5_math.DifferentialWrapped360(goalPos, currentPos)
                # directionVector = DiffWrapDeg(goalPos - currentPos)
                if item is not self.parent.base: #Probably not needed
                    if directionVector < 0:
                        if currentPos < item.getVariable('misc variables', 'cwAngleLimit')/DEG_TO_CYTRON_CONVERT:
                            limitDistance = currentPos + 360 - item.getVariable('misc variables', 'cwAngleLimit')/DEG_TO_CYTRON_CONVERT
                        else:
                            limitDistance = currentPos - item.getVariable('misc variables', 'cwAngleLimit')/DEG_TO_CYTRON_CONVERT
                    else:
                        if currentPos > item.getVariable('misc variables', 'ccwAngleLimit')/DEG_TO_CYTRON_CONVERT:
                            limitDistance = item.getVariable('misc variables', 'ccwAngleLimit')/DEG_TO_CYTRON_CONVERT + 360 - currentPos
                        else:
                            limitDistance = item.getVariable('misc variables', 'ccwAngleLimit')/DEG_TO_CYTRON_CONVERT - currentPos
                    if abs(directionVector) > limitDistance:
                        if directionVector > 0:
                            directionVector -= 360
                        else:
                            directionVector += 360
                #We have the direction and magnitude now.... tedious
                #If acceleration distance has not been determined, then now determine it
                #if not item.checkVariable('feedback variables','approachDist'):
                    #There is no approach dist yet, need to dev it

                #Determine if  we are accelerating or cruising or decelerating
                #Determine dist travelled
                limitDistance = self._stamps['time difference'] * desiredSpeed * self.tuner
                #Determine if dist travelled is overshoot
                if limitDistance > abs(directionVector):
                    newCurrentPos = goalPos
                else:
                    if directionVector < 0:
                        limitDistance *= -1
                    newCurrentPos = orion5_math.wrap360f(currentPos + limitDistance)

                # if item is self.parent.shoulder:
                #     print(newCurrentPos)
                #     newCurrentPos *= orion5_math.SHOULDER_GEAR_RATIO

                item.setVariable('feedback variables', 'currentPosition', newCurrentPos)
