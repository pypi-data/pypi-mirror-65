import os
import glob
import logging
import sys
import serial
import serial.tools.list_ports as list_ports
import time
import platform
import threading

# http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
def serialList():
    """Lists serial ports
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    serialPortList = []
    for port in list_ports.comports():
        if port.pid and port.vid:
            serialPortList.append({'name': port.description, 'type':'serial', 'peripheralId': port.device, 'pid': port.pid, 'vid': port.vid})

    return serialPortList

logger = logging.getLogger(__name__)

class serialRead(threading.Thread):
    def __init__(self,ser,cb):
        self.ser = ser
        self.cb = cb
        self.running = True
        self.rawMode = False
        self.t = time.clock()
        threading.Thread.__init__(self)
    
    def run(self):
        while self.running:
            try:
                # l = self.ser.readline().decode('utf-8')
                # print("read: "+l) receive log
                c = self.ser.read(64)
                if c:
                    dt = (time.clock() - self.t)*1000000
                    self.cb(c, dt)
                    self.t = time.clock()
            except Exception as err:
                logger.warn("Serial Read error %s" %err)
                self.running = False
                self.cb(None, -1)

class serialCom():
    def __init__(self,rxCallback):
        self.rxcb = rxCallback
        self.ser = None
        self.rxth = None
        return
    
    def connect(self,port,baud=115200, timeout=0.05):
        self.ser = serial.Serial(port, baud, timeout=timeout)
        #todo: separate serial reading to different threads
        self.rxth = serialRead(self.ser,self.rxcb)
        self.rxth.setDaemon(True)
        self.rxth.start() 
        return
    
    def close(self):
        if self.rxth:
            self.rxth.running = False
        if self.ser:
            self.ser.close()
        self.rxth = None
        self.ser = None
        
    def write(self,msg):
        if self.ser == None:
            return
        self.ser.write(msg)
        # print("send: "+msg) # send log
