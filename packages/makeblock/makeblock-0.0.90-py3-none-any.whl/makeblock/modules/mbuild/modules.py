# -*- coding: utf-8 -*
import struct
from time import ctime, sleep
import threading
from makeblock.utils import *
from makeblock.protocols.PackData import NeuronPackData

class _BaseModule:
    def __init__(self,board,idx=1,mode=1,period=0):
        self._pack = None
        self.setup(board,idx,mode,period)
        
    def _callback(self,data):
        pass

    def setup(self,board,idx,mode=1,period=0):
        self._board = board
        self._mode = mode
        self._pack = NeuronPackData()
        self._pack.idx = idx
        self._init_module()
        # if self._pack.type==NeuronPackData.TYPE_SENSOR:
        #     self._pack.data = [0x7f,mode]
        #     self._pack.data.extend(long2bits(period))
        #     self.request(self._pack)
    
    def _init_module(self):
        pass

    def force_update(self):
        self._pack.data = [0x1]
        self.request(self._pack)

    def request(self,pack):
        self._board.remove_response(pack)
        self._board.request(pack)

    def call(self,pack):
        self._board.call(pack)

    def subscribe(self,pack):
        self._board.request(pack)

class Temperature(_BaseModule):
    def _init_module(self):
        self._temperature = 0
        self._pack.type = NeuronPackData.TYPE_SENSOR
        self._pack.service = 0x63
        self._pack.subservice = 0x1
        self._pack.on_response = self.__on_parse
        
    def __on_parse(self, pack):
        self._temperature = bits2float(pack.data[1:6])
        self._callback(self._temperature)

    def on_change(self,callback):
        self._callback = callback

    @property
    def temperature(self):
        return self._temperature

class Humiture(_BaseModule):
    def _init_module(self):
        self._pack.type = NeuronPackData.TYPE_SENSOR
        self._pack.service = 0x63
        self._pack.subservice = 0x19
        self._pack.on_response = self.__on_parse
        self._status = {"temp":0,"hum":0}
        
    def __on_parse(self, pack):
        self._status["temp"] = bits2short(pack.data[1:3])
        self._status["hum"] = pack.data[3]
        self._callback(self._status)

    def on_change(self,callback):
        self._callback = callback

    @property
    def temperature(self):
        return self._status["temp"]
    
    @property
    def humiture(self):
        return self._status["hum"]

class Ultrasonic(_BaseModule):
    def _init_module(self):
        self._distance = 0
        self._pack.type = NeuronPackData.TYPE_SENSOR
        self._pack.service = 0x63
        self._pack.subservice = 0x16
        self._pack.on_response = self.__on_parse
        
    def __on_parse(self, pack):
        self._distance = bits2float(pack.data[1:6])
        self._callback(self._distance)

    def on_change(self,callback):
        self._callback = callback

    def request_distance(self,callback):
        self._pack.on_response = callback
        self.force_update()

    @property
    def distance(self):
        return self._distance

class Slider(_BaseModule):
    def _init_module(self):
        self._value = 0
        self._pack.type = NeuronPackData.TYPE_SENSOR
        self._pack.service = 0x64
        self._pack.subservice = 0xd
        self._pack.on_response = self.__on_parse
        
    def __on_parse(self, pack):
        if len(pack.data)>1:
            self._value = pack.data[1]
            self._callback(self._value)

    def on_change(self,callback):
        self._callback = callback

    def request_value(self,callback):
        self._callback = callback
        self.force_update()

    @property
    def value(self):
        return self._value

class RGBLed(_BaseModule):
    def _init_module(self):
        self._pack = NeuronPackData()
    
    def set_color(self,red,green,blue):
        self._pack.service = 0x65
        self._pack.subservice = 0x2
        self._pack.data = [0x1]
        self._pack.data.extend(short2bits(red))
        self._pack.data.extend(short2bits(green))
        self._pack.data.extend(short2bits(blue))
        self.call(self._pack)
    
class LedStrip(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x65
        self._pack.subservice = 0x3
    
    def set_color(self,index,red,green,blue):
        self._pack.data = [0x1,index]
        self._pack.data.extend(short2bits(red))
        self._pack.data.extend(short2bits(green))
        self._pack.data.extend(short2bits(blue))
        self.call(self._pack)

class LedMatrix(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x65
        self._pack.subservice = 0x9
    
    def set_pixel(self,index,red,green,blue):
        self._pack.data = [0x2,index]
        self._pack.data.extend(short2bits(red))
        self._pack.data.extend(short2bits(green))
        self._pack.data.extend(short2bits(blue))
        self.call(self._pack)
    
    def set_pixels(self,bits,red,green,blue):
        self._pack.data = [0x1]
        for i in range(2):
            self._pack.data.extend(long2bits(bits[i]))
        self._pack.data.extend(short2bits(red))
        self._pack.data.extend(short2bits(green))
        self._pack.data.extend(short2bits(blue))
        self.call(self._pack)

    def set_string(self,msg):
        l = len(msg)
        self._pack.data = [0x7]
        self._pack.data.extend(short2bits(l))
        for i in range(l):
            self._pack.data.append(ord(msg[i]))
        self.call(self._pack)

class Servo(_BaseModule):
    BOTH_SERVOS = 1
    LEFT_SERVO = 2
    RIGHT_SERVO = 3
    def _init_module(self):
        self._pack = NeuronPackData()
        self._pack.service = 0x62
        self._pack.subservice = 0xa
    
    def set_angle(self,angle):
        angle = int(angle)
        self._pack.data = [0x1]
        self._pack.data.extend(short2bits(angle))
        self.call(self._pack)
    
    def release(self):
        self._pack.data = [0x6]
        self.call(self._pack)

class Speaker(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x66
        self._pack.subservice = 0x4

    def play_tone(self,hz):
        self._pack.data = [0x2]
        self._pack.data.extend(short2bits(hz))
        self.call(self._pack)

class FingertipPiano(_BaseModule):
    '''
        :description: Fingertip Piano
        :example:
        .. code-block:: python
            :linenos:

            piano = FingertipPiano(1)

    '''
    def _init_module(self):
        self._isExiting = False
        self._pack.service = 0x64
        self._pack.subservice = 0xf
        self._piano = {'touch1_strength':0,'touch2_strength':0,'touch3_strength':0,'touch4_strength':0,'keyA':0,'keyB':0,'touch1':0,'touch2':0,'touch3':0,'touch4':0,'joystick_x':0,'joystick_y':0,'distance':0,'keyA_count':0,'keyB_count':0,'last_touched':0,'last_pressed':0,'gesture':0}
        self.subscribe_all()
        self._thread = threading.Thread(target=self._thread_detect,args=())
        self._thread.start()
        self._board.add_thread(self)

    def exit(self):
        self._isExiting = True
        self._thread.join()

    def _thread_detect(self):
        while True:
            if self._isExiting:
                break
            self._detecting()
            sleep(0.1)

    def _detecting(self):
        # print("detecting")
        pass
    def __on_parse(self, pack):
        pass

    def on_subscribe_response(self,pack):
        if pack.data[0]==0x2:
            self._piano['keyA'] = pack.data[1]
            self._piano['keyB'] = pack.data[2]
        elif pack.data[0]==0x3:
            self._piano['touch1'] = pack.data[1]
            self._piano['touch2'] = pack.data[2]
            self._piano['touch3'] = pack.data[3]
            self._piano['touch4'] = pack.data[4]
        elif pack.data[0]==0x6:
            self._piano['gesture'] = pack.data[1]
        elif pack.data[0]==0x5:
            self._piano['joystick_x'] = bits2int8(pack.data[1:3])
            self._piano['joystick_y'] = bits2int8(pack.data[3:5])
        elif pack.data[0]==0x7:
            self._piano['distance'] = pack.data[1]
        elif pack.data[0]==0x8:
            self._piano['touch1_strength'] = bits2short(pack.data[1:3])
            self._piano['touch2_strength'] = bits2short(pack.data[3:5])
            self._piano['touch3_strength'] = bits2short(pack.data[5:7])
            self._piano['touch4_strength'] = bits2short(pack.data[7:9])
        elif pack.data[0]==0x9:
            self._piano['keyA_count'] = bits2long(pack.data[1:6])
            self._piano['keyB_count'] = bits2long(pack.data[6:11])

    def subscribe_all(self):
        pack = NeuronPackData()
        pack.on_response = self.on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE,0,0,0,0]
        self.subscribe(pack)
        pack.data = [0x7e,NeuronPackData.TYPE_CHANGE,0,0,0,0]
        self.subscribe(pack)
        pack.data = [0x7d,NeuronPackData.TYPE_CHANGE,0,0,0,0]
        self.subscribe(pack)
        pack.data = [0x7c,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(long2bits(200))
        self.subscribe(pack)
        pack.data = [0x7b,NeuronPackData.TYPE_CHANGE,0,0,0,0]
        self.subscribe(pack)
        pack.data = [0x7a,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(long2bits(200))
        self.subscribe(pack)
        pack.data = [0x78,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(long2bits(200))
        self.subscribe(pack)
        pack.data = [0x79,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(long2bits(200))
        self.subscribe(pack)

    def count_pressed(self,idx):
        """
            :description: count of button pressed

            :param idx: button number, 'A' or 'B' 
            :type idx: str
            :return: count
            :rtype: int
            :example:

            .. code-block:: python
                :linenos:

                while True:
                    print(piano.count_pressed('A'),piano.count_pressed('B'))
                    sleep(1)

        """
        if idx==1 or idx.lower()=='a':
            return self._piano['keyA_count']
        if idx==2 or idx.lower()=='b':
            return self._piano['keyB_count']

    def is_pressed(self,idx):
        """
            :description: the status will changed when the button is pressed
            :param idx: the button number, 'A' or 'B' 
            :type idx: str
            :return: whether the button is pressed
            :rtype: int
            :example:

            .. code-block:: python
                :linenos:

                while True:
                    print(piano.is_pressed('A'),piano.is_pressed('B'))
                    sleep(1)

        """
        if idx==1 or (type(idx)==str and idx.lower()=='a'):
            return self._piano['keyA']
        if idx==2 or (type(idx)==str and idx.lower()=='b'):
            return self._piano['keyB']

    @property
    def is_obstacle_ahead(self):
        return self.distance<95

    @property
    def obstacle_moving(self):
        return self.gesture

    def last_pressed(self,idx=0):
        if idx==1:
            idx = 'A'
        elif idx==2:
            idx = 'B'
        if idx==0:
            if (self._piano['keyA']+self._piano['keyB'])==0 and self._piano['last_pressed']!=idx:
                self._piano['last_pressed']=idx
                return 0
        elif self._piano['key'+idx] and self._piano['last_pressed']!=idx:
            self._piano['last_pressed']=idx
            return 0
        return 1

    def touch_value(self,idx):
        if idx==1 or (type(idx)==str and idx.lower()=='a'):
            return int(self._piano['touch1_strength']*100/256)
        elif idx==2 or (type(idx)==str and idx.lower()=='b'):
            return int(self._piano['touch2_strength']*100/256)
        elif idx==3 or (type(idx)==str and idx.lower()=='c'):
            return int(self._piano['touch3_strength']*100/256)
        elif idx==4 or (type(idx)==str and idx.lower()=='d'):
            return int(self._piano['touch4_strength']*100/256)

    def is_touched(self,idx):
        """
            :description: the status will changed when the touchpad is touched
            :param idx: the touchpad number, range: 1~4 
            :type idx: int
            :return: whether the touchpad is touched
            :rtype: int
            :example:

            .. code-block:: python
                :linenos:

                while True:
                    print(piano.is_touched(1),piano.is_touched(2))
                    sleep(1)

        """
        if idx==1 or (type(idx)==str and idx.lower()=='a'):
            return self._piano['touch1']
        elif idx==2 or (type(idx)==str and idx.lower()=='b'):
            return self._piano['touch2']
        elif idx==3 or (type(idx)==str and idx.lower()=='c'):
            return self._piano['touch3']
        elif idx==4 or (type(idx)==str and idx.lower()=='d'):
            return self._piano['touch4']

    def last_touched(self,idx=0):
        if idx==0:
            if self._piano['touch4']+self._piano['touch1']+self._piano['touch2']+self._piano['touch3']==0 and self._piano['last_touched']!=idx:
                self._piano['last_touched']=idx
                return 0
        elif self._piano['touch'+str(idx)] and self._piano['last_touched']!=idx:
            self._piano['last_touched']=idx
            return 0
        return 1

    @property
    def gesture(self):
        return self._piano['gesture']

    @property
    def distance(self):
        return self._piano['distance']

    @property
    def ir_intensity(self):
        return 100 - self.distance

    @property
    def joystick_x(self):
        return self._piano['joystick_x']

    @property
    def joystick_y(self):
        return self._piano['joystick_y']

    @property
    def joystick_direction(self):
        if self.is_joystick_up:
            return self.DIRECTION_UP
        elif self.is_joystick_down:
            return self.DIRECTION_DOWN
        elif self.is_joystick_left:
            return self.DIRECTION_LEFT
        elif self.is_joystick_right:
            return self.DIRECTION_RIGHT
        return self.DIRECTION_HOME

    @property
    def is_joystick_up(self):
        return self._piano['joystick_y']>30

    @property
    def is_joystick_down(self):
        return self._piano['joystick_y']<-30

    @property
    def is_joystick_left(self):
        return self._piano['joystick_x']<-30

    @property
    def is_joystick_right(self):
        return self._piano['joystick_x']>30
        
    @property
    def DIRECTION_HOME(self):
        return 0

    @property
    def DIRECTION_UP(self):
        return 1

    @property
    def DIRECTION_DOWN(self):
        return 2

    @property
    def DIRECTION_LEFT(self):
        return 3

    @property
    def DIRECTION_RIGHT(self):
        return 4

    @property  
    def GESTURE_NONE(self):
        return 0

    @property  
    def GESTURE_WAVING(self):
        return 1
    
    @property  
    def GESTURE_MOVING_DOWN(self):
        return 2

    @property  
    def GESTURE_MOVING_UP(self):
        return 3

    @property
    def APPROACHING(self):
        return self.GESTURE_MOVING_DOWN

    @property
    def AWAY(self):
        return self.GESTURE_MOVING_UP

    def set_led(self,red=0,green=0,blue=0):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x1]
        pack.data.extend(short2bits(red))
        pack.data.extend(short2bits(green))
        pack.data.extend(short2bits(blue))
        self.call(pack)

    def led_on(self,red=0,green=0,blue=0):
        self.set_led(red,green,blue)

    def led_off(self):
        self.set_led(0,0,0)

    def reset_button(self,idx=2):
        self.reset_button(idx)

    def reset_pressed(self,idx=2):
        if type(idx)==str:
            if idx.lower()=='a':
                idx = 0
            elif idx.lower()=='b':
                idx = 1
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x11,idx]
        self.call(pack)
    
    def calibrate(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x10]
        self.call(pack)