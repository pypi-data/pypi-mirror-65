import socket
import time
import select
import traceback
from threading import Event, Lock, Thread

from . import utils
from . import orion5_math


PING_INTERVAL = 0.5


class IntervalTimer(Thread):
    def __init__(self, function, interval):
        Thread.__init__(self)
        self.stop_event = Event()
        self.function = function
        self.interval = interval


    def stop(self):
        self.stop_event.set()


    def run(self):
        while not self.stop_event.wait(self.interval):
            self.function()



class Orion5Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.timeouts = 0
        self.lock = Lock()
        self.timer = IntervalTimer(self._ping, PING_INTERVAL)


    def stop(self):
        print('stopping')
        # self._write('0+trySetFlag+0+')
        time.sleep(1)
        self.timer.stop()
        self.socket.close()
        print('stopped')


    def connect(self, timer=True):
        self.socket.connect((utils.SOCKET_HOST, utils.SOCKET_PORT))
        if timer:
            self._start_ping()


    def _start_ping(self):
        self.timer.start()


    def _set_flag(self):
        with self.lock:
            self._write('0+trySetFlag+1+')
            data = self._read()
            data = data.split('+')[1]
            return data == '1'


    def _ping(self):
        if self.lock.acquire(False):
            self._write('p')
            data = self._read()
            self.lock.release()
            return data


    def _write(self, data):
        self.socket.sendall(('$' + '{:03d}'.format(len(data)) + '&' + str(data)).encode())


    def _read(self):
        try:

            read_buffer = ''
            while True:
                data = ''
                ready = select.select([self.socket], [], [], 1)
                if ready[0]:
                    data = self.socket.recv(1024).decode()
                    if len(data) > 0:
                        read_buffer += data
                        if '$' in read_buffer:
                            split = read_buffer.split('$')
                            for e in split:
                                if len(e) > 4:
                                    e = e.split('&')
                                    length = int(e[0])
                                    if len(e[1]) == length:
                                        read_buffer = read_buffer[5+length:]
                                        self.timeouts = 0
                                        return e[1]
                    else:
                        self.timeouts += 1
                        if self.timeouts > utils.SOCKET_MAX_TIMEOUTS:
                            self.stop()
                            print('Orion5Client Timeout')

        except Exception as e:
            print('Orion5Client:', e)
            traceback.print_tb(e.__traceback__)
            self.stop()


    def getVar(self, jointID, id1, id2):
        with self.lock:
            to_send = str(jointID) + '+' + id1 + '+' + id2
            self._write(to_send)
            data = self._read()
            data = data.split('+')
            id1 = data[0]
            data = data[1]
            if id1 == 'posFeedback' or id1 == 'velFeedback' or id1 == 'torFeedback':
                try:
                    return eval(data)
                except:
                    print('eval error:', data)
                    return 'eval error'
            else:
                return float(data)


    def setVar(self, jointID, id1, id2, value):
        with self.lock:
            if id1 == 'posControl':
                value = [float(round(e, 2)) for e in value]
            elif id1 == 'velControl':
                value = [int(e) for e in value]
            elif id1 == 'enControl':
                value = [int(e) for e in value]
            else:
                value = str(value)

            to_send = str(jointID) + '+' + id1 + '+' + id2 + '+' + str(value)
            self._write(to_send)


    def releaseTorque(self):
        self.setAllJointsTorqueEnable([0, 0, 0, 0, 0])


    def enableTorque(self):
        self.setAllJointsTorqueEnable([1, 1, 1, 1, 1])


    def setAllJointsPosition(self, angles):
        angles = [orion5_math.wrap360f(angle) for angle in angles]
        self.setVar(0, 'posControl', '', angles)


    def setAllJointsSpeed(self, speeds):
        self.setVar(0, 'velControl', '', speeds)


    def setAllJointsTorqueEnable(self, enables_in):
        enables = []
        for e in enables_in:
            if e:
                enables.append(1)
            else:
                enables.append(0)
        self.setVar(0, 'enControl', '', enables)


    def getAllJointsPosition(self):
        return self.getVar(0, 'posFeedback', '')


    def getAllJointsSpeed(self):
        return self.getVar(0, 'velFeedback', '')


    def getAllJointsLoad(self):
        return self.getVar(0, 'torFeedback', '')


    def getAllJointsError(self):
        return self.getVar(0, 'errFeedback', '')
