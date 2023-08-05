# -*- coding: utf-8 -*
from makeblock.boards.meorion.modules import *
from makeblock.boards.base import _BaseEngine
import makeblock.protocols as Protocols

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

def create(device):
    return MeOrion(device)

class MeOrion(_BaseEngine):
    def __init__(self,device):
        super().__init__(device,Protocols.MegaPiProtocol())
