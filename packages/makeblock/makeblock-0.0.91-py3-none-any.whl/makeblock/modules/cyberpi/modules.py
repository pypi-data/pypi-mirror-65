# -*- coding: utf-8 -*
import json
import makeblock.utils
from makeblock.protocols.PackData import HalocodePackData

class _BaseModule:
    def __init__(self,board,index=0):
        self._pack = None
        self.setup(board,index)
        
    def _callback(self,data):
        pass

    def setup(self,board,index):
        self._board = board
        self._index = index
        self._init_module()
    
    def _init_module(self):
        pass

    def request(self,pack):
        self._board.remove_response(pack)
        self._board.request(pack)

    def call(self,pack):
        self._board.call(pack)
    
    def send_script(self,mode,script):
        '''
            发送py代码
        '''
        self._pack.mode = mode
        self._pack.script = script
        if mode==HalocodePackData.TYPE_RUN_WITHOUT_RESPONSE:
            self.call(self._pack)
        if mode==HalocodePackData.TYPE_RUN_WITH_RESPONSE:
            self.request(self._pack)

    def subscribe(self,pack):
        '''
            订阅数据
        '''
        self._board.subscribe(pack)

    def unsubscribe(self,pack):
        '''
            取消订阅
        '''
        self._board.unsubscribe(pack)

class RGBLed(_BaseModule):
    def _init_module(self):
        self._pack = HalocodePackData()
        self._pack.type = HalocodePackData.TYPE_SCRIPT

    def set_color(self,index,red,green,blue):
        script = "led.show_single({0},{1},{2},{3})".format(index,red,green,blue)
        self.send_script(HalocodePackData.TYPE_RUN_WITHOUT_RESPONSE,script)

    def set_colors(self,red,green,blue):
        script = "led.show_all({0},{1},{2})".format(red,green,blue)
        self.send_script(HalocodePackData.TYPE_RUN_WITHOUT_RESPONSE,script)

    def set_full_colors(self,colors):
        script = "led.show_full_color({0})".format(colors)
        self.send_script(HalocodePackData.TYPE_RUN_WITHOUT_RESPONSE,script)

class Button(_BaseModule):
    def _init_module(self):
        self._pack = HalocodePackData()
        self._pack.on_response = self.__on_parse 
        self._is_pressed = False
        self.subscribe_pressed() #订阅按钮状态

    def __on_parse(self, pack):
        try:
            ret = eval("".join([ chr(i) for i in pack.data[3:len(pack.data)]]))
            if not ret['ret'] is None:
                self._is_pressed = ret['ret']
                if not self._callback is None:
                    self._callback(ret["ret"])
        except:
            print("error")
        else:
            pass

    @property
    def is_pressed(self):
        return self._is_pressed

    def on_subscribe_response(self,pack):
        self._is_pressed = pack.subscribe_value

    def request_pressed(self,callback):
        self._callback = callback
        self._pack.type = HalocodePackData.TYPE_SCRIPT
        script = "button.is_pressed()"
        self.send_script(HalocodePackData.TYPE_RUN_WITH_RESPONSE,script) #主动请求按钮状态数据

    def subscribe_pressed(self):
        pack = HalocodePackData()
        pack.type = HalocodePackData.TYPE_SCRIPT
        pack.script = "subscribe.add_item({0}, button.is_pressed, ())"
        pack.mode = HalocodePackData.TYPE_RUN_WITH_RESPONSE
        pack.on_response = self.on_subscribe_response #状态上报结果回调，用于解析数据
        self.subscribe(pack)