from .pac_const import *
import enum


class PacketDecoder(object):
    class _Status(enum.IntEnum):
        HEADER = 0
        COMMAND = 1
        TOCKEN = 2
        LENGTH = 3
        DATA = 4
        CHKSUM = 5

    _header_buffer = b'\x00\x00\x00'
    _counter = int()
    _command = int()
    _length = int()
    _data = bytes()
    _chksum = int()
    _isError = bool()
    _isDone = bool()

    def __init__(self):
        super(PacketDecoder, self).__init__()
        self._status = self._Status(self._Status.HEADER)

    def step(self, ch):

        if self._status is self._Status.HEADER:
            self._header_buffer = self._header_buffer[1:3] + bytes([ch])
            if self._header_buffer == HEADER:
                self._chksum = 0
                self._status = self._Status.COMMAND

        elif self._status is self._Status.COMMAND:
            self._command = Command(ch)
            self._counter = 0
            self._status = self._Status.TOCKEN

        elif self._status is self._Status.TOCKEN:
            self._status = self._Status.LENGTH

        elif self._status is self._Status.LENGTH:
            self._counter = self._counter + 1
            if self._counter == 1:
                self._length = ch << 8
            elif self._counter == 2:
                self._length += ch
                self._counter = 0
                self._data = b''
                if self._length == 0:
                    self._status = self._Status.CHKSUM
                else:
                    self._status = self._Status.DATA

        elif self._status is self._Status.DATA:
            self._chksum += ch
            self._counter = self._counter + 1
            self._data += bytes([ch])
            if self._counter == self._length:
                self._status = self._Status.CHKSUM

        elif self._status is self._Status.CHKSUM:
            if self._chksum % 256 != ch:
                self._error = True
            self._status = self._Status.HEADER
            self._header_buffer = b'\x00\x00\x00'
            self._isDone = True

    def isDone(self):
        return self._isDone

    def isError(self):
        return self._isError

    def getPacket(self):
        if self.isDone():
            res = {
                'command': self._command,
                'data': self._data
            }
            self._isDone = False
            return res
        else:
            res = {
                'command': None,
                'data': b''
            }
            return res
