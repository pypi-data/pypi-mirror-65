# -*- coding: utf-8 -*
import struct
import time
from time import ctime, sleep
import makeblock.utils

from makeblock.protocols.PackData import MegaPiPackData

class _BaseModule:
    def __init__(self,board,port=0,slot=0):
        self._pack = None
        self.setup(board,port,slot)
        
    def _callback(self,data):
        pass

    def setup(self,board,port=0,slot=0):
        self._init_module()
        self._board = board
        self._pack.port = port
        self._pack.slot = slot

    def request(self,pack):
        self._board.remove_response(pack)
        self._board.request(pack)

    def call(self,pack):
        self._board.call(pack)

class HaloOnBoard(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x8

    def set_pixel(self,index,red,green,blue):
        self._pack.data = [0x0,0x2,index]
        self._pack.data.append(red)
        self._pack.data.append(green)
        self._pack.data.append(blue)
        self.call(self._pack)

    def set_pixels(self,pixels):
        self._pack.data = [0x0,0x2,1]
        self._pack.data.extend(pixels)
        self.call(self._pack)

class DCMotor(_BaseModule):
    """
        DCMotor

        :param board: 主控板
        :param port: Port口，取值范围：PORT1～PORT4
        :param slot: Slot口，取值范围：SLOT1～SLOT2
    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x0A

    def run(self,speed):
        """
            run

            :param speed: 速度比值，取值范围：-255～255
        """
        self._pack.data = [self._pack.port]
        self._pack.data.extend(makeblock.utils.short2bytes(speed))
        self.call(self._pack)
        
class LightSensorOnBoard(_BaseModule):
    """
        板载光线传感器
    """
    SENSOR_1 = 1
    SENSOR_2 = 2
    def _init_module(self):
        self._temperature = 0
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 3
        self._pack.on_response = self.__on_parse
        
    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def on_change(self,callback):
        self._callback = callback

    def read(self,index,callback):
        """
            请求数据

            :param index: 序号 (LightSensorOnBoard.SENSOR_1~2)
            :type index: int
            :param callback: 回调函数
            :type callback: function
        """
        self._callback = callback
        if index==LightSensorOnBoard.SENSOR_1:
            self._pack.data = [12,2]
        if index==LightSensorOnBoard.SENSOR_2:
            self._pack.data = [11,2]
        self.request(self._pack)

class Light(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x03
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)