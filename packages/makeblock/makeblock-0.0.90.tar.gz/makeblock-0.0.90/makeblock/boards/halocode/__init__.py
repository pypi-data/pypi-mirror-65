# -*- coding: utf-8 -*
from time import sleep
from ...modules.halocode import *
from ...boards.base import _BaseEngine
from ...protocols.PackData import HalocodePackData
from ...comm.SerialPort import SerialPort
from ...comm import mlink
MODE_REQUEST = 0
MODE_CHANGE = 1
MODE_PERIOD = 2
board = None

def create(device=None,channel=None):
    global board
    if type(device)==int:
        channel = device
    if not board is None:
        return board
    if channel is None:
        channels = mlink.list()
        if len(channels)>0:
            device = mlink.create(channels[0])
            board = Modules(device)
            return board
    else:
        device = mlink.create(channel)
        board = Modules(device)
        return board
    if device is None:
        ports = [port[0] for port in SerialPort.list() if port[2] != 'n/a' and port[2].find('1A86:7523')>0 ]
        if len(ports)>0:
            device = SerialPort(ports[0])
            board = Modules(device)
            return board
    '''
        :description: Halocode - |halocode_more_info|

        .. |halocode_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/halocode/en/tutorials/introduction.html" target="_blank">More Info</a>
            
        :example:
        .. code-block:: python
            :linenos:

            from time import sleep
            from makeblock import SerialPort
            from makeblock import Halocode

            uart = SerialPort.create("COM3")
            board = Halocode.create(uart)

    '''
    return Modules(device)
    
class Modules(_BaseEngine):
    def __init__(self,device):
        self._led = None
        self._button = None
        self._pin0 = None
        self._pin1 = None
        self._pin2 = None
        self._pin3 = None
        self._motion = None
        self._microphone = None
        super().__init__(_BaseEngine.Halocode,device)
        if device.type!='mlink':
            while not self.protocol.ready:
                self.broadcast()
                sleep(0.3)
        self.setTransferMode()

    def setTransferMode(self):
        self.repl("global_objects.communication_o.enable_protocol(global_objects.communication_o.REPL_PROTOCOL_GROUP_ID)")
        sleep(1)
        pack = HalocodePackData.broadcast()
        self.call(pack)
        self.repl('import communication')
        self.repl('communication.bind_passthrough_channels("uart0", "uart1")')

    def broadcast(self):
        pack = HalocodePackData()
        pack.type = HalocodePackData.TYPE_SCRIPT
        pack.mode = HalocodePackData.TYPE_RUN_WITH_RESPONSE
        pack.script = ""
        self.call(pack)
    
    def set_led(self,idx,red,green,blue):
        '''
        :description: set rgb led's color on board

        :example:

        .. code-block:: python
            :linenos:

            while True:
                board.set_led(0,30,0,0)
                sleep(0.5)
                board.set_led(0,0,30,0)
                sleep(0.5)
                board.set_led(0,0,0,30)
                sleep(0.5)
        ''' 
        if self._led is None:
            self._led = Halo(self)
        self._led.set_color(idx,red,green,blue)

    def set_leds(self,red,green,blue):
        '''
        :description: set rgb leds' colors on board

        :example:

        .. code-block:: python
            :linenos:

            while True:
                board.set_leds(30,0,0)
                sleep(0.5)
                board.set_leds(0,30,0)
                sleep(0.5)
                board.set_leds(0,0,30)
                sleep(0.5)
        ''' 
        if self._led is None:
            self._led = Halo(self)
        self._led.set_colors(red,green,blue)

    def set_full_leds(self,colors):
        if self._led is None:
            self._led = Halo(self)
        self._led.set_full_colors(colors)

    @property
    def is_pressed(self):
        '''
        :description: whether Button on board is pressed

        :example:

        .. code-block:: python
            :linenos:

            while True:
                print(board.is_pressed)
                sleep(0.1)
        '''     
        if self._button is None:
            self._button = Button(self)
        return self._button.is_pressed

    def _init_pin(self,pin):
        if pin==0:
            if self._pin0 is None:
                self._pin0 = Pin(self,0)
            return self._pin0
        elif pin==1:
            if self._pin1 is None:
                self._pin1 = Pin(self,1)
            return self._pin1
        elif pin==2:
            if self._pin2 is None:
                self._pin2 = Pin(self,2)
            return self._pin2
        elif pin==3:
            if self._pin3 is None:
                self._pin3 = Pin(self,3)
            return self._pin3

    def is_touched(self,pin_number):
        '''
        :description: set pin input as touchpad

        :param pin_number: range:0~3
        :type pin_number: int
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                board.is_touched(2)
                sleep(1)
        '''     
        pin = self._init_pin(pin_number)
        return pin.is_touched

    def write_digital(self,pin_number,level):
        '''
        :description: set pin output as digital pin

        :example:

        .. code-block:: python
            :linenos:

            while True:
                board.write_digital(2,0)
                sleep(1)
                board.write_digital(2,1)
                sleep(1)
        '''     
        pin = self._init_pin(pin_number)
        pin.write_digital(pin_number,level)

    def write_pwm(self,pin_number,pwm):
        '''
        :description: set pin output as pwm pin

        :param pin_number: range:0~3
        :type pin_number: int
        :param pwm: range:0~255
        :type pwm: int
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                board.write_pwm(2,100)
                sleep(1)
                board.write_pwm(2,0)
                sleep(1)
        '''
        pin = self._init_pin(pin_number)
        pin.write_pwm(pin_number,pwm)

    def write_servo(self,pin_number,angle):
        '''
        :description: set pin output as pulse pin for servo driving

        :param pin_number: range:0~3
        :type pin_number: int
        :param pwm: range:0~180
        :type pwm: int
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                board.write_servo(2,120)
                sleep(1)
                board.write_servo(2,60)
                sleep(1)
        '''
        pin = self._init_pin(pin_number)
        pin.servo_write(pin_number,angle)

    def read_digital(self,pin_number,callback):
        '''
        :description: set pin input as digital pin

        :param pin_number: range:0~3
        :type pin_number: int
        :param callback: callback
        :type callback: function
        
        :example:

        .. code-block:: python
            :linenos:

            def on_read(value):
                print("level:",value)
            while True:
                board.read_digital(2,on_read)
                sleep(1)
        '''
        pin = self._init_pin(pin_number)
        pin.read_digital(callback)

    def read_analog(self,pin_number,callback):
        '''
        :description: set pin input as analog pin

        :param pin_number: range:0~3
        :type pin_number: int
        :param callback: callback
        :type callback: function
        
        :example:

        .. code-block:: python
            :linenos:

            def on_read(value):
                print("value:",value)
            while True:
                board.read_analog(2,on_read)
                sleep(1)
        '''
        pin = self._init_pin(pin_number)
        pin.read_analog(callback)

    @property
    def is_shaked(self):
        return self.is_shaking
        
    @property
    def is_shaking(self):
        '''
        :description: whether the halocode is shaked
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("is shaking:",board.is_shaking)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
        return self._motion.is_shaking

    @property
    def roll(self):
        '''
        :description: the halocode's roll degree
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("roll:",board.roll)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
        return self._motion.roll

    @property
    def yaw(self):
        '''
        :description: the halocode's yaw degree
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("yaw:",board.yaw)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
        return self._motion.yaw

    @property
    def pitch(self):
        '''
        :description: the halocode's pitch degree
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("pitch:",board.pitch)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
        return self._motion.pitch

    @property
    def shake_level(self):
        '''
        :description: the strength level of shaking
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("shake_level:",board.shake_level)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
        return self._motion.shake_strength

    @property
    def loudness(self):
        '''
        :description: loudness from the microphone on board
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("loudness:",board.loudness)
                sleep(0.1)
        '''
        if self._microphone is None:
            self._microphone = Microphone(self)
        return self._microphone.loudness

    @property
    def is_pitch_up(self):
        '''
        :description: whether motion status is pitch up
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("is_pitch_up:",board.is_pitch_up)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
            return 0
        return self._motion.pitch<-15
    @property
    def is_pitch_down(self):
        '''
        :description: whether motion status is pitch down
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("is_pitch_down:",board.is_pitch_down)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
            return 0
        return self._motion.pitch>15
    @property
    def is_roll_left(self):
        '''
        :description: whether motion status is roll left
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("is_roll_left:",board.is_roll_left)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
            return 0
        return self._motion.roll<-15

    @property
    def is_roll_right(self):
        '''
        :description: whether motion status is roll right
        
        :example:

        .. code-block:: python
            :linenos:

            while True:
                print("is_roll_right:",board.is_roll_right)
                sleep(0.1)
        '''
        if self._motion is None:
            self._motion = Motion(self)
            return 0
        return self._motion.roll>15