# -*- coding: utf-8 -*
from time import sleep
from ...modules.cyberpi import *
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
        :description: CyberPi - |cyberpi_more_info|

        .. |cyberpi_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/halocode/en/tutorials/introduction.html" target="_blank">More Info</a>
            
        :example:
        .. code-block:: python
            :linenos:

            from time import sleep
            from makeblock import CyberPi

            board = CyberPi.create()

    '''
    return Modules(device)
    
class Modules(_BaseEngine):
    def __init__(self,device):
        self._led = None
        self._button = None
        super().__init__(_BaseEngine.Halocode,device)
        if device.type!='mlink':
            while not self.protocol.ready:
                self.broadcast()
                sleep(0.5)
        sleep(1)
        self.setTransferMode()
        sleep(1)

    def setTransferMode(self):
        # pack = HalocodePackData()
        # pack.type = HalocodePackData.TYPE_SCRIPT
        # pack.mode = HalocodePackData.TYPE_RUN_WITHOUT_RESPONSE
        # pack.script = "global_objects.communication_o.enable_protocol(global_objects.communication_o.REPL_PROTOCOL_GROUP_ID)"
        # self.call(pack)
        # sleep(1)
        self.repl('import communication')
        self.repl('communication.bind_passthrough_channels("uart0", "uart1")')
        sleep(1)

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
            self._led = RGBLed(self)
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
            self._led = RGBLed(self)
        self._led.set_colors(red,green,blue)

    def set_full_leds(self,colors):
        if self._led is None:
            self._led = RGBLed(self)
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