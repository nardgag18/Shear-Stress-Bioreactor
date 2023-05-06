import serial
import time

class serialConnect():
    def __init__(self):
        self.debug = True
        
        if(self.debug == True):
            port = '/dev/cu.usbserial-028603D9'
        else:
            port = '/dev/ttyACM0'
        


    def readSerial():
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)

    def writeSerial(msg):
        ser.write(str(msg).encode('utf-8'))



if __name__ == '__main__' :
    #/dev/cu.usbserial-028603D9
    #ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    #ser = serial.Serial('/dev/cu.usbserial-028603D9', 9600, timeout=1)
    #ser.reset_input_buffer()

    '''
    while True:
        code = 
    '''