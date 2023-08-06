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

    def _init_module(self):
        pass

    def request(self,pack):
        self._board.remove_response(pack)
        self._board.request(pack)

    def call(self,pack):
        self._board.call(pack)
