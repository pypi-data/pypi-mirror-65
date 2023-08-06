# -*- coding: utf-8 -*
from ...modules.rj25 import *
from ...boards.base import _BaseEngine
from ...comm.SerialPort import SerialPort
from ...comm import mlink

PORT1 = 1
PORT2 = 2
PORT3 = 3
PORT4 = 4
PORT5 = 5
PORT6 = 6
PORT7 = 7
PORT8 = 8
SLOT1 = 1
SLOT2 = 2
SLOT3 = 3
SLOT4 = 4
M9 = 9
M10 = 10
M11 = 11
M12 = 12
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
    """
    :description: Mega Pi Pro Board - |mega_pi_pro_more_info|

    .. |mega_pi_pro_more_info| raw:: html
    
        <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/main-control-boards/megapi-pro.html" target="_blank">More Info</a>

    :example:
    .. code-block:: python
        :linenos:

        from time import sleep
        from makeblock import SerialPort
        from makeblock import MegaPiPro

        uart = SerialPort.create("COM3")
        board = MegaPiPro.create(uart)

    """
    return Modules(device)

class Modules(_BaseEngine):
    """

    """
    def __init__(self,device):
        super().__init__(_BaseEngine.MegaPi,device)

    def Servo(self,port,slot):
        """
            :description: Servo Driver - |servo_more_info|

            .. |servo_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/adapters/me-rj25-adapter.html" target="_blank">Me RJ25 Adapter</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/meds15-servo-motor.html" target="_blank">MEDS15 Servo</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/9g-micro-servo.html" target="_blank">9g Micro Servo</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/mg995-standard-servo.html" target="_blank">MG995 Servo</a>

            :param port: Port Number, range：PORT5～PORT8
            :type port: int
            :param slot: Slot Number, range：SLOT1～SLOT2
            :type slot: int

            :example:
                
            .. code-block:: python
                :linenos:

                servo = board.Servo(PORT6,SLOT1)

        """
        return Servo(self,port,slot)

    def DCMotor(self,*argv):
        """
            :description: DC Motor Driver - |dc_motor_more_info|

            .. |dc_motor_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">MegaPi Encoder/DC Motor Driver</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/36-dc-geared-motor-12v240rpm.html" target="_blank">36 DC Geared Motor 12V 240RPM</a> |
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/dc-motor-25-6v.html" target="_blank">DC Motor-25 6V</a> |
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/dc-motor-37-12v.html" target="_blank">DC Motor-37 12V</a> |
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/mini-metal-gear-motor-n20-dc-12v.html" target="_blank">Mini Metal Gear Motor – N20 DC 12V</a> |
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/tt-geared-motor-dc-6v-200rpm.html" target="_blank">TT Geared Motor DC 6V-200RPM</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/air-pump-motor-dc-12v-3202pm.html" target="_blank">Air Pump Motor DC 12V-3202PM</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/micro-peristaltic-pump-dc12-0v.html" target="_blank">Micro Peristaltic Pump DC12.0V</a> |
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/air-pump-motor-dc-12v-370-02pm.html" target="_blank">Air Pump Motor – DC 12V-370-02PM</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/water-pump-motor-dc-12v-370-04pm.html" target="_blank">Water Pump Motor – DC 12V-370-04PM</a>
                
            :param port: Port Number, range: PORT1～PORT4
            :type port: int
            :param slot: Slot Number, range: SLOT1～SLOT2
            :type slot: int

            :example:

            .. code-block:: python
                :linenos:

                dcmotor = board.DCMotor(MegaPi.PORT1,MegaPi.SLOT1)

        """
        return DCMotor(self,*argv)

    def StepperMotor(self,slot):
        """
            :description: Stepper Motor Driver - |stepper_more_info|

            .. |stepper_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-stepper-motor-driver.html" target="_blank">More Info</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/42byg-stepper-motor.html" target="_blank">42BYG Stepper Motor</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/42byg-geared-stepper-motor.html" target="_blank">42BYG Geared Stepper Motor</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/57byg-stepper-motor.html" target="_blank">57BYG Stepper Motor</a>

            :param slot: Slot Number, range: SLOT1～SLOT4
            :type slot: int

            :example:

            .. code-block:: python
                :linenos:

                stepper = board.StepperMotor(SLOT1)

        """
        return StepperMotor(self,slot)

    def EncoderMotor(self,slot):
        """
            :description: Encoder Motor Driver - |encoder_more_info|

            .. |encoder_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">More Info</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/dc-encoder-motor-25-6v-185rpm.html" target="_blank">DC Encoder Motor – 25 6V-185RPM</a>

            :param slot: Slot Number, range: SLOT1～SLOT4
            :type slot: int

            :example:

            .. code-block:: python
                :linenos:

                encoder = board.EncoderMotor(SLOT1)

        """
        return EncoderMotor(self,slot)

    def SmartServo(self,port=5):
        """
            :description: Smart Servo Driver

            :example:

            .. code-block:: python
                :linenos:

                smartservo = board.SmartServo()

        """
        return SmartServo(self,port)
    
    def BLDCMotor(self,port=1):
        """
            :description: BLDC Motor Driver

            :example:

            .. code-block:: python
                :linenos:

                bldc = board.BLDCMotor()

        """
        return BLDCMotor(self,port)
    
    def RGBLed(self,port,slot=2):
        """
            :description: RGB Led Driver - |rgbled_more_info|

            .. |rgbled_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/displays/me-rgb-led.html" target="_blank">Me RGB LED</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/adapters/me-rj25-adapter.html" target="_blank">Me RJ25 Adapter</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/displays/led-rgb-strip-addressable-sealed-0-5m1m.html" target="_blank">LED RGB Strip</a> | 

            :param port: Port Number, range: PORT5~PORT8
            :type port: int
            :param slot: Slot Number when using led rgb strip, range: SLOT1～SLOT2
            :type slot: int

            :example:

            .. code-block:: python
                :linenos:

                rgbled = board.RGBLed(board,PORT6)

        """
        return RGBLed(self,port,slot)

    def SevenSegmentDisplay(self,port):
        """
            :description: Seven Segment Display - |7segdisplay_more_info|

            .. |7segdisplay_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/displays/me-7-segment-display.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                sevseg = board.SevenSegmentDisplay(PORT6)

        """
        return SevenSegmentDisplay(self,port)

    def LedMatrix(self,port):
        """
            :description: LED Matrix Display - |ledmatrix_more_info|

            .. |ledmatrix_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/displays/me-led-matrix-8x16.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                ledmatrix = board.LedMatrix(PORT6)

        """
        return LedMatrix(self,port)

    def DSLRShutter(self,port):
        """
            :description: Shutter for DSLR - |shutter_more_info|

            .. |shutter_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/execution/me-shutter.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                shutter = board.DSLRShutter(PORT6)

        """
        return DSLRShutter(self,port)
    
    def InfrareReceiver(self,port):
        """
            :description: Infrare Receiver - |infrare_more_info|

            .. |infrare_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/communicators/me-infrared-reciver-decode.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                ir = board.InfrareReceiver(PORT6)

        """
        return InfrareReceiver(self,port)

    def Ultrasonic(self,port):
        """
            :description: Ultrasonic Sensor - |ultrasonic_more_info|

            .. |ultrasonic_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-ultrasonic-sensor.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                us = board.Ultrasonic(PORT6)

        """
        return Ultrasonic(self,port)

    def Button(self,port):
        """
            :description: Button - |button_more_info|

            .. |button_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/control/me-4-button.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                button = board.Button(PORT6)

        """
        return Button(self,port)

    def LineFollower(self,port):
        """
            :description: LineFollower - |linefollower_more_info|

            .. |linefollower_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-line-follower.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                linefollower = board.LineFollower(PORT6)

        """
        return LineFollower(self,port)

    def LimitSwitch(self,port,slot=2):
        """
            :description: LimitSwitch - |limitswitch_more_info|

            .. |limitswitch_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/adapters/me-rj25-adapter.html" target="_blank">Me RJ25 Adapter</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-micro-switch-ab.html" target="_blank">Me Micro Switch A</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int
            :param slot: Slot Number, range: SLOT1~SLOT2
            :type slot: int

            :example:

            .. code-block:: python
                :linenos:

                limitswitch = board.LimitSwitch(MegaPi.PORT6,MegaPi.SLOT1)

        """
        return LimitSwitch(self,port,slot)

    def PIRMotion(self,port):
        """
            :description: PIR Motion - |pirmotion_more_info|

            .. |pirmotion_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-pir-motion-sensor.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                pir = board.PIRMotion(PORT6)

        """
        return PIRMotion(self,port)

    def Light(self,port):
        """
            :description: Light Sensor - |light_more_info|

            .. |light_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-light-sensor.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                light = board.Light(PORT6)

        """
        return Light(self,port)
    
    def Sound(self,port):
        """
            :description: Sound Sensor - |sound_more_info|

            .. |sound_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-sound-sensor.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                sound = board.Sound(PORT6)

        """
        return Sound(self,port)

    def Potentiometer(self,port):
        """
            :description: Potentiometer - |potentiometer_more_info|

            .. |potentiometer_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/control/me-potentiometer.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                potentiometer = board.Potentiometer(MegaPi.PORT6)

        """
        return Potentiometer(self,port)

    def Joystick(self,port):
        """
            :description: Joystick - |joystick_more_info|

            .. |joystick_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/control/me-joystick.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                joystick = board.Joystick(PORT6)

        """
        return Joystick(self,port)

    def Gyro(self):
        """
            :description: Gyro Sensor - |gyro_more_info|

            .. |gyro_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-3-axis-accelerometer-and-gyro-sensor.html" target="_blank">More Info</a>

            :example:

            .. code-block:: python
                :linenos:

                gyro = board.Gyro()

        """
        return Gyro(self)

    def Compass(self):
        """
            :description: Compass Sensor - |compass_more_info|

            .. |compass_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-compass.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                compass = board.Compass(PORT6)

        """
        return Compass(self)

    def Temperature(self,port,slot):
        """
            :description: Temperature - |temperature_more_info|

            .. |temperature_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/adapters/me-rj25-adapter.html" target="_blank">Me RJ25 Adapter</a> | 
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/temperature-sensor-waterproofds18b20.html" target="_blank">Me Temperature Sensor</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int
            :param slot: Slot Number, range: SLOT1~SLOT2
            :type slot: int

            :example:

            .. code-block:: python
                :linenos:

                temp = board.Temperature(PORT6,SLOT1)

        """
        return Temperature(self,port,slot)

    def Humiture(self,port):
        """
            :description: Humiture Sensor - |humiture_more_info|

            .. |humiture_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-temperature-and-humidity-sensor.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                humiture = board.Humiture(PORT6)

        """
        return Humiture(self,port)

    def Flame(self,port):
        """
            :description: Flame Sensor - |flame_more_info|

            .. |flame_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-flame-sensor.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                flame = board.Flame(PORT6)

        """
        return Flame(self,port)

    def Gas(self,port):
        """
            :description: Gas Sensor - |gas_more_info|

            .. |gas_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-gas-sensormq2.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                gas = board.Gas(PORT6)

        """
        return Gas(self,port)

    def Touch(self,port):
        """
            :description: Touch Sensor - |touch_more_info|

            .. |touch_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-touch-sensor.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                touch = board.Touch(PORT6)

        """
        return Touch(self,port)

    def Color(self,port):
        """
            :description: Color Sensor - |color_more_info|

            .. |color_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-color-sensor-v1.html" target="_blank">More Info</a>

            :param port: Port Number, range: PORT5~PORT8
            :type port: int

            :example:

            .. code-block:: python
                :linenos:

                color = board.Color(PORT6)

        """
        return Color(self,port)

    def Pin(self):
        """
            :description: Pin - |pin_more_info|

            .. |pin_more_info| raw:: html
            
                <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/main-control-boards/megapi.html" target="_blank">More Info</a>

            :example:

            .. code-block:: python
                :linenos:

                pin = board.Pin()

        """
        return Pin(self)