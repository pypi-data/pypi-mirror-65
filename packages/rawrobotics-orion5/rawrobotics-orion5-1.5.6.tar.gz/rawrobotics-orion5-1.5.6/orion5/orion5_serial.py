import threading
import serial
import time
import struct
import traceback

from . import utils
from . import orion5_math


class SerialThread(threading.Thread):
    '''
    Need to create an incoming and outgoing dynamic buffer.

    The main loop should first check if the usb is connected, if not then it should attempt connection
    If the main loop is connected, then the main functionality ensues, disconnection should be handled
    dynamically.
    In the main loop one of the modules should pull all of the incomming USB buffer into the software buffer
    A module after that one should pull all meaningful packets out of the software buffer
    Following this there is the outbound comms...   this will get complex:
    There should be an outgoing buffer, it will be something like [timeout, [bytes]], when a set of bytes
    is sent through, the timeout is set to current system time or whatever. After this we have almost start
    condition again; all messages to be sent will be polled up in this buffer, so the main loops requests
    to the ORION5 will go into here, any checkers to be returned will go into here, etc. If the buffer gets
     larger than 64bytes? then send the first/last... dyslexia 64bytes through and reset the timeout. If
     the timeout value vs the now time exceeds a certain time, then push what is in there through.

     The Checker...  The PC will send checker bytes in its packets, they will be handled the same on both
     pc and ORION5 sides...  When the pc side here receives a packet, it will take the checker and add it
     to a registry of checkers. a seperate module in the main loop called the bureaucrat, will look at this
     registry and build 'a' packet or multiple packets (if greater than 64bytes or some arbitrary number),
     of checkerlist packettypes which it will dump into the outbound buffer.

     when the pc receives a checkerlist packettype, it will go through the flag variable in the joint
     dictionaries and
    '''
    def __init__(self, orion5_reference, serialName):
        threading.Thread.__init__(self)
        self._outboxIterator = [
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
        self._globalConstIterator = [
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

        self.arm = orion5_reference
        self._outboxIterator2 = []
        for item1 in self._outboxIterator:
            #print('item1',type(item1))
            for item2 in item1[1]:
                #print(type(item2))
                for item3 in range(0, 5):
                    self._outboxIterator2.append([self.arm.joints[item3], item1[0], item2[0], item2[1], item2[2], item3, True, 0])
        for item in self._globalConstIterator:
            item.append(False)
            item.append(0)
            self._outboxIterator2.append(item)
        self.running = True
        self.uart = None
        self._lastFeedbackTime = 0
        self._requestFeedback = 1
        self._checker = [2, [], 0, 0]
        self._received = {'ErrorCodes':0, 'RequestFeedback':0, 'ResendSpeed':500}
        self._constants = {'ResendSpeedMax':200, 'ResendSpeedMin':20, 'ResendSpeedWin':-1, 'ResendSpeedLose':20, 'debug': 0}
        ############Debug####################
        if self._constants['debug']:
            print(self._outboxIterator2, len(self._outboxIterator2))
        #####################################
        try:
            self.uart = serial.Serial(
                port=serialName,
                baudrate=utils.SERIAL_BAUD_RATE,
                write_timeout=0,
                timeout=utils.SERIAL_TIMEOUT
            )
        except Exception as e:
            print(e)
            utils.debug("SerialThread: Unable to find serial device")
            utils.debug("SerialThread: Thread will immediately exit")
            self.stop()


    def run(self):
        if self.uart is None:
            return
        utils.debug("SerialThread: Thread started")
        try:
            self.main()
        except Exception as e:
            print('exception in main:', e)
            traceback.print_tb(e.__traceback__)
        self.uart.close()
        self.stop()
        utils.debug("SerialThread: Thread stopped")


    def stop(self):
        self.arm.setVariable('firmwareVersion', -1)
        self.arm.setVariable('serialNum', -1)
        if self.running:
            utils.debug("SerialThread: Stopping thread")
            self.running = False
        else:
            utils.debug("SerialThread: Thread already stopped")

    def RequestFirmwareVersion(self):
        self.SendPacket(self.BuildPacket(6, 0, [], 'asking for firmware version again'))

    def RequestSerialNum(self):
        self.SendPacket(self.BuildPacket(8, 0, [], 'asking for serial number again'))

    def main(self):
        self.SendPacket(self.BuildPacket(6, 0, [], 'Request firmare version'))
        self.SendPacket(self.BuildPacket(8, 0, [], 'Request serial number'))

        while self.running:

            # print('\n\n BORK \n\n', self.uart.in_waiting)

            self._checker[2] -= 1 #tune XXXX

            ############Debug####################
            if self._constants['debug'] and False:
                print('Checkers existent', len(self._outboxIterator2))
                for item in self._outboxIterator2:
                    if item[-1]:
                        if item[-2]:
                            print('The checks still here', item[-1], item[-3],
                                item[1], item[2], item[0].checkVariable(item[1], item[2]))
                        else:

                            print('The checks still here', item[-1], item[0])
                print(' ')
            #################################################

            # look through joint registries for new data
            if self._checker[2] < 250:
                for i in range(20):
                    if self._checker[3] >= len(self._outboxIterator2):
                        self._checker[3] = 0
                        if self._received['RequestFeedback'] <= 1:
                            self.RequestFeedback(True)
                            if len(self._checker[1]) > 0:
                                temp7 = []
                                for item in self._checker[1]:
                                    temp7.append((item & 0xFF00) >> 8)
                                    temp7.append(item & 0xFF)
                                self.SendPacket(self.BuildPacket(7, len(temp7), temp7, 'CheckerSet third shake', 0))
                        self._received['RequestFeedback'] = 0
                    item = self._outboxIterator2[self._checker[3]]
                    self._checker[3] += 1
                    if item[-2]:
                        if item[0].checkVariable(item[1], item[2]):
                            ID = item[0].getVariable('constants', 'ID')
                            value = item[0].getVariable(item[1], item[2])
                            # convert to G15 angle if var is a position update
                            if item[2] == 'goalPosition':
                                value = orion5_math.Deg360ToG15Angle(value)
                            # firmware workaround for time-to-goal mode
                            if item[2] == 'desiredSpeed' and item[0].getVariable('control variables', 'controlMode') == utils.ControlModes.TIME:
                                '''#wtf?... hmmmmm   setting first and 4th bits? control reasons? XXXX
                                this value is x10? because? I know it goes /10 inside the g15 and is turned into a float...
                                is that to make it an int, int math.. yes that would be it'''
                                value = (int(value * 10) & 0x1FFF) | 0x8000
                            if  item[-1]:
                                self.ProcessSend((ID, item[3], item[4], value, self._checker[0]), item[2], ' Joint Data '+str(item), item[-1])
                            else:
                                self.CheckerAdvance()
                                self.ProcessSend((ID, item[3], item[4], value, self._checker[0]), item[2], ' Joint Data '+str(item), self._checker[0])
                                item[-1] = 0 + self._checker[0]
                            break
                    else:
                        if self.arm.checkVariable(item[0]):
                            value = self.arm.getVariable(item[0])  #_globalConstants[item[0]][0]
                            if item[0] == 'mode':
                                if  item[-1]:
                                    packet = self.BuildPacket(5, 3, [0x45, value & 0xFF, (value & 0xFF00) >> 8], 'Mode', item[-1])
                                else:
                                    self.CheckerAdvance()
                                    packet = self.BuildPacket(5, 3, [0x45, value & 0xFF, (value & 0xFF00) >> 8], 'Mode', self._checker[0])
                                    item[-1] = 0 + self._checker[0]
                            else:
                                if  item[-1]:
                                    packet = self.BuildPacket(4, 3, [item[1], value & 0xFF, (value & 0xFF00) >> 8], 'Not Mode?', item[-1])
                                else:
                                    self.CheckerAdvance()
                                    packet = self.BuildPacket(4, 3, [item[1], value & 0xFF, (value & 0xFF00) >> 8], 'Not Mode?', self._checker[0])
                                    item[-1] = 0 + self._checker[0]
                            self.SendPacket(packet)
                            if item[0] == 'firmwareUpdate':
                                self.stop()
                                break
                            break

            numPacketsRead = 0
            while self.uart.in_waiting > 8:
                self.ProcessRead()
                numPacketsRead += 1
                if numPacketsRead > utils.SERIAL_MAX_PACKETS_PROCESSED:
                    break

            time.sleep(utils.SERIAL_SLEEP)


    def CheckerAdvance(self):
        # Advance the Checker
        if self._checker[0] >= 65500:
            self._checker[0] = 2
        else:
            self._checker[0] += 1


    def ProcessSend(self, command, name, source = ' Huhu ', oldChecker = -1):
        data = [command[0], command[1], (command[3] & 0xFF)]
        if command[2] == 2:
            data.append((command[3] & 0xFF00) >> 8)
        packet = self.BuildPacket(0, 2 + command[2], data, 'ProcessSend'+ source, oldChecker) #need to add checker in???  XXXX
        retValue = self.SendPacket(packet)
        '''print(name, command[3])
        for e in packet:
            print(e, end=', ')
        print('\n\n')'''
        # time.sleep(0.1)
        return retValue


    def RequestFeedback(self, thing = False):
        if thing:
            self.SendPacket(self.BuildPacket(2, 0, [], 'RequestFeedback', -1))
        else:
            self.SendPacket(self.BuildPacket(2, 0, [], 'RequestFeedback', 0))


    def RequestErrorCodes(self, index):
        self.SendPacket(self.BuildPacket(1, 2, [index, 16], 'RequestErrorCodes', -1))


    def StopFeedback(self):
        self.SendPacket(self.BuildPacket(3, 0, [], 'StopFeedback', -1))


    def GetChecksum(self, packet):
        sum1 = 0
        sum2 = 0

        for index in range(len(packet)):
            sum1 = (sum1 + packet[index]) % 255
            sum2 = (sum2 + sum1) % 255

        return (sum2 << 8) | sum1


    def ProcessRead(self):
        # print('\n\n\nOKAY\n\n\n')
        valid = 0
        state = 0
        reset = 0
        byte = 0
        checksum1 = 0
        checksum2 = 0
        packetType1 = 0
        packetType2 = 0
        checker = 0
        data = []
        feedbackRequests = 0
        speed = 0

        while True:
            if self.uart.in_waiting == 0:
                break
            try:
                byte = struct.unpack('B', self.uart.read(1))[0]
            except Exception as e:
                print(e)
                print('could not read byte')
                break

            if state < utils.SERIAL_HEADER_LEN:
                # grab header bytes
                if byte == utils.SERIAL_USB_HEADER[state]:
                    state += 1
                else:
                    reset = 1;
            elif state == utils.SERIAL_HEADER_LEN + 0:
                # grab packet type 1
                packetType1 = byte
                state += 1
            elif state == utils.SERIAL_HEADER_LEN + 1:
                # grab packet type 2
                packetType2 = byte
                state += 1
            elif state == utils.SERIAL_HEADER_LEN + 2:
                # grab data bytes
                if len(data) == packetType2:
                    state += 1
                else:
                    data.append(byte)
            if state == utils.SERIAL_HEADER_LEN + 3:
                checker = byte
                state += 1
            elif state == utils.SERIAL_HEADER_LEN + 4:
                # first checksum byte
                checksum1 = byte
                state += 1
            elif state == utils.SERIAL_HEADER_LEN + 5:
                # second checksum byte
                checksum2 = byte
                valid = (self.GetChecksum(utils.SERIAL_USB_HEADER + [packetType1, packetType2] + data + [checker]) == ((checksum1 << 8) | checksum2))
                if not valid:
                    #print('reeeeeeeeeeeeeeeeeeeeeeeeee')
                    reset = 1

            if valid:
                break

            if reset:
                # reset state vars
                valid = 0
                state = 0
                reset = 0
                checksum1 = 0
                checksum2 = 0
                data = []

        if valid:

            if packetType1 == 0x36:
                # 0x36 is one register from G15
                # print(data)
                value = 0
                if len(data) == 3:
                    value = data[2] # struct.unpack('B', data[2])[0]
                elif len(data) == 4:
                    value = struct.unpack('<H', bytes(data[2:4]))[0]

                if data[1] == 0:
                    self.arm.joints[data[0]].setVariable('feedback variables', 'currentPosition', orion5_math.G15AngleTo360(value))
                elif data[1] == 1:
                    self.arm.joints[data[0]].setVariable('feedback variables', 'currentVelocity', value)
                elif data[1] == 2:
                    self.arm.joints[data[0]].setVariable('feedback variables', 'currentLoad', value)
                elif data[1] == 16:
                    self.arm.joints[data[0]].setVariable('misc variables', 'error', value)
                    # print('error from servo {0}: value: {1}'.format(data[0], value))

            elif packetType1 == 0x22:
                # 0x22 is all feedback vars from all G15s
                self._received['RequestFeedback'] += 1
                unpacked = struct.unpack('HHHHHHHHHHHHHHH', bytes(data))
                for i in range(len(self.arm.joints)):
                    position = orion5_math.G15AngleTo360(unpacked[i*3+0])
                    #if i == 1:
                    #    print(unpacked[i*3+0], position, position / 2.857)
                    self.arm.joints[i].setVariable('feedback variables', 'currentPosition', position)
                    self.arm.joints[i].setVariable('feedback variables', 'currentVelocity', unpacked[i*3+1])
                    self.arm.joints[i].setVariable('feedback variables', 'currentLoad', unpacked[i*3+2])

            elif packetType1 == 0x89:
                unpacked = struct.unpack('I', bytes(data))[0]
                self.arm.setVariable('firmwareVersion', unpacked)
                # print('Orion5 Firmware Version:', self.arm.getVariable('firmwareVersion'))

            elif packetType1 == 0x90:
                unpacked = struct.unpack('I', bytes(data))[0]
                unpacked = unpacked & 0xFFFFFF
                self.arm.setVariable('serialNum', unpacked)
                # print('Orion5 Serial Number:', self.arm.getVariable('serialNum'))

            elif packetType1 == 0x08:
                #Pull out the arms USB incomming buffer size
                self._checker[2] = data[-2] | (data[-1] << 8)
                self._checker[1] = []
                #Pull out ESTOP here data[-3]
                if not self.arm.checkVariable('Estop') and self.arm.getVariable('Estop') != data[-3]:
                    # print('Estop IN', self.arm.checkVariable('Estop'), self.arm.getVariable('Estop'), data)
                    self.arm.setVariable('Estop', data[-3])
                #Check if there are any checkers in this second handshake packet
                if len(data) > 3:
                    for iterator1 in range(0, len(data)-3, 2):
                        if data[iterator1] | (data[iterator1+1] << 8) == 0:
                            continue
                        self._checker[1].append(data[iterator1] | (data[iterator1+1] << 8))
                        ############Debug####################
                        if self._constants['debug'] and False:
                            print('The Checker!!', data, self._checker)
                        #####################################
                        # look through joint registries for checkers
                        for item in self._outboxIterator2:
                            ############Debug####################
                            if self._constants['debug'] and False:
                                if item[-1] != 0:
                                    print('The checks still here', item)
                            ############################
                            if self._checker[1][-1] == item[-1]:
                                ############Debug####################
                                if self._constants['debug']:
                                        print('WOOOOOOO', item)
                                #####################################
                                item[-1] = 0
                                if item[-2]:
                                    item[0].setTick(item[1], item[2], 0)

                                else:
                                    self.arm.setTick(item[0], 0)
                                break
                    # print('\n\n\nYEE\n\n\n')
                    ############Debug####################
                    if self._constants['debug']:
                        print('The Checker!!', len(data), data, self._checker)
                    #####################################


    def BuildPacket(self, type, length, data, source = 'Haha', oldChecker = -1):
        # <0xF0> <0xF0> <packetType1> <packetType2> <data 1> ... <data n> <checksum>
        # 0x69 - 105 - set variable in registry
        # 0x36 - 54 - request a var from registry
        # 0x22 - 34 - request all feedback vars from all G15s
        # 0x24 - 36 - stop all feedback vars
        # 0x42 - 66 - write global constant
        # 0x08 - 08 - Checker Send
        # 0x89 - 137 - send firmware thing pls
        # 0x90 - 138 - send serial number

        hexReg = [0x69, 0x36, 0x22, 0x24, 0x42, 0x99, 0x89, 0x08, 0x90]
        packet = utils.SERIAL_USB_HEADER + [hexReg[type], length]
        for i in range(len(data)):
            packet.append(data[i])
        if oldChecker == -1:
            #packet.append(oldChecker)
            #else:
            self.CheckerAdvance()
            oldChecker = 0 + self._checker[0]#packet.append(self._checker[0])
        packet.append((oldChecker & 0xFF00) >> 8)
        packet.append(oldChecker & 0xFF)
        ############Debug####################
        if self._constants['debug']:
            print(self._checker[0], type, length, data, source, oldChecker)
        #####################################
        checksum = self.GetChecksum(packet)
        packet.append((checksum & 0xFF00) >> 8)
        packet.append(checksum & 0xFF)
        #print(packet)
        return bytes(packet)


    def SendPacket(self, packet):
        if self.uart is None:
            utils.debug("SerialThread: SendPacket: uart is None")
            return False
        try:
            self.uart.write(packet)
            #time.sleep(0.25)
            return True
        except serial.SerialTimeoutException:
            utils.debug("SerialThread: SendPacket: timeout writing to serial port")
            return False
