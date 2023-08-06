
import progressbar
import argparse
import serial
import time
import enum

from asaloader.pac_const import Command
from asaloader.pac_decoder import PacketDecoder
from asaloader.pac_encoder import pac_encode
from asaloader.device import device_list
from asaloader.ihex import parseIHex, cut_to_pages, resize_to_page
from asaloader.locale import _

class CommandTrnasHandler():
    def __init__(self, ser):
        self._ser = ser
        self._pd = PacketDecoder()
        self.timeout = 5

    def _get_packet(self):
        start_time = time.clock()
        exec_time = 0
        exit_flag = False
        pac_decode_err_flag = False
        packet = None

        while exec_time < 3 and exit_flag is False:
            ch = self._ser.read(1)

            if len(ch) != 0:
                self._pd.step(ch[0])

            if self._pd.isDone():
                packet = self._pd.getPacket()
                exit_flag = True
            elif self._pd.isError():
                pac_decode_err_flag = True
                exit_flag = True
            exec_time = time.clock() - start_time

        if exec_time > self.timeout:
            print(_('timeout error'))
            # TODO exception
            raise Exception

        if pac_decode_err_flag:
            print(_('packet decode error'))
            # TODO exception
            raise Exception

        return packet

    def _put_packet(self, cmd, data):
        req = {
            'command': cmd,
            'data': data
        }
        req_raw = pac_encode(req)
        self._ser.write(req_raw)


    def cmd_chk_protocol(self):
        self._put_packet(Command.CHK_PROTOCOL, b'test')
        rep = self._get_packet()

        if rep['command'] == Command.ACK1 and rep['data'] == b'OK!!':
            return True, 1
        elif rep['command'] == Command.CHK_PROTOCOL and rep['data'][0] == 0:
            return True, rep['data'][1]
        else:
            return False

    # commands for v1
    def cmd_v1_enter_prog(self):
        res, version = self.cmd_chk_protocol()
        if res and version == 1:
            return True

    def cmd_v1_flash_write(self, page_data):
        # v1 寫入 flash 不會有回應，且下次寫入需要等待 0.03 s
        self._put_packet(Command.DATA, page_data)
        return True
    
    def cmd_v1_prog_end(self):
        self._put_packet(Command.DATA, b'')
        rep = self._get_packet()

        if rep['command'] == Command.ACK2 and rep['data'] == b'OK!!':
            return True
        else:
            return False

    # commands for v2
    def cmd_v2_enter_prog(self):
        res, version = self.cmd_chk_protocol()
        if res and version == 2:
            return True

    def cmd_v2_prog_chk_device(self):
        self._put_packet(Command.PROG_CHK_DEVICE, b'')
        rep = self._get_packet()

        if rep['command'] == Command.PROG_CHK_DEVICE and rep['data'][0] == 0:
            return True, rep['data'][1]
        else:
            return False

    def cmd_v2_prog_end(self):
        self._put_packet(Command.PROG_END, b'')
        rep = self._get_packet()

        if rep['command'] == Command.PROG_END and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_prog_end_and_go_app(self):
        self._put_packet(Command.PROG_END_AND_GO_APP, b'')
        rep = self._get_packet()

        if rep['command'] == Command.PROG_END_AND_GO_APP and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_prog_set_go_app_delay(self, t):
        self._put_packet(Command.PROG_SET_GO_APP_DELAY, t.to_bytes(2, 'little'))
        rep = self._get_packet()

        if rep['command'] == Command.PROG_SET_GO_APP_DELAY and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_flash_set_pgsz(self, size):
        self._put_packet(Command.FLASH_SET_PAGE_SZ, size.to_bytes(4, 'little'))
        rep = self._get_packet()
        if rep['command'] == Command.FLASH_SET_PAGE_SZ and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_flash_get_pgsz(self):
        self._put_packet(Command.FLASH_GET_PAGE_SZ, b'')
        rep = self._get_packet()
        if rep['command'] == Command.FLASH_GET_PAGE_SZ and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:3], 'little')
        else:
            return False

    def cmd_v2_flash_write(self, page_addr, data):
        paylod = page_addr.to_bytes(4, 'little') + data
        self._put_packet(Command.FLASH_WRITE, paylod)
        rep = self._get_packet()
        if rep['command'] == Command.FLASH_WRITE and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_flash_read(self):
        self._put_packet(Command.FLASH_READ, b'')
        rep = self._get_packet()
        if rep['command'] == Command.FLASH_READ and rep['data'][0] == 0:
            return True, rep['data']
        else:
            return False

    def cmd_v2_flash_earse_sector(self, num):
        self._put_packet(Command.FLASH_EARSE_SECTOR, num.to_bytes(2, 'little'))
        rep = self._get_packet()
        if rep['command'] == Command.FLASH_EARSE and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:5], 'little')
        else:
            return False

    def cmd_v2_flash_earse_all(self):
        self._put_packet(Command.FLASH_EARSE_ALL, b'')
        rep = self._get_packet()
        if rep['command'] == Command.FLASH_EARSE_ALL and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_eep_set_pgsz(self, size):
        self._put_packet(Command.EEPROM_SET_PAGE_SZ,
                         size.to_bytes(4, 'little'))
        rep = self._get_packet()
        if rep['command'] == Command.EEPROM_SET_PAGE_SZ and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_eep_get_pgsz(self):
        self._put_packet(Command.EEPROM_GET_PAGE_SZ, b'')
        rep = self._get_packet()
        if rep['command'] == Command.EEPROM_GET_PAGE_SZ and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:3], 'little')
        else:
            return False

    def cmd_v2_eep_write(self, page_data):
        self._put_packet(Command.EEPROM_WRITE, page_data)
        rep = self._get_packet()
        if rep['command'] == Command.EEPROM_WRITE and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:5], 'little')
        else:
            return False

    def cmd_v2_eep_read(self):
        self._put_packet(Command.EEPROM_READ, b'')
        rep = self._get_packet()
        if rep['command'] == Command.EEPROM_READ and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:5], 'little')
        else:
            return False

    def cmd_v2_eep_earse(self):
        self._put_packet(Command.EEPROM_EARSE, b'')
        rep = self._get_packet()
        if rep['command'] == Command.EEPROM_EARSE and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:5], 'little')
        else:
            return False

    def cmd_v2_eep_earse_all(self):
        self._put_packet(Command.EEPROM_EARSE_ALL, b'')

        rep = self._get_packet()
        if rep['command'] == Command.EEPROM_EARSE_ALL and rep['data'][0] == 0:
            return True
        else:
            return False


class Loader():
    class _State(enum.IntEnum):
        SET_PARA   = 0
        FLASH_PROG = 1
        EEP_PROG = 2
        END = 3

    def __init__(self, ser, args):
        self._args = args
        self._ser = ser
        self._cth = CommandTrnasHandler(ser)

        self.device_type = args.device_type
        self._chk_device()

        self.st_list = list()

        self.is_prog_flash = args.is_prog_flash
        self.flash_page_index = 0

        self.is_prog_eep = args.is_prog_eep
        self.eep_page_index = 0

        self.total_steps = 0
        self.cur_step = 0

        if args.is_prog_flash:
            res = parseIHex(args.flash_file)
            res = resize_to_page(res, 256)
            self.flash_pages = cut_to_pages(res, 256)
            self.st_list += [self._State.FLASH_PROG]
            self.total_steps += len(self.flash_pages)
    
        if args.is_prog_eep:
            # 切割 eeprom data 成數頁，一頁 256 bytes
            self.eep_data = eep_data
            pgsz = 256
            self._cth.cmd_v2_eep_set_pgsz(8)
            self.eep_pages = [eep_data[i:i+pgsz] for i in range(0, len(eep_data), pgsz)]

            # eeprom 未滿一個頁面，補0xFF
            if len(self.eep_pages[-1]) != pgsz:
                l = pgsz-len(self.eep_pages[-1])
                self.eep_pages[-1] += b''.join([b'\xFF' for i in range(0, l)])

            # 在狀態機中加入燒錄 eeprom 動作
            self.st_list += [self._State.EEP_PROG]
            self.total_steps += len(self.eep_pages)
        
        self._is_go_app = args.is_go_app
        self._go_app_delay = args.go_app_delay

        self.st_list += [self._State.END]
        self.total_steps += 1

        self.status = 0
    
    def _chk_device(self):
        res, ver = self._cth.cmd_chk_protocol()

        if res is False:
            print(_('ERROR: Can\'t communicate with tje device.'))
            print(_('       Please check the comport is correct.'))
        
        # auto detect device
        if device_list[self.device_type]['protocol_version'] == 0:
            if res and ver == 1:
                print(_('Detect device is \'asa_m128_v1\' or \'asa_m128_v2\''))
                self.device_type = 2
            if res and ver == 2:
                res, self.device_type = self._cth.cmd_v2_prog_chk_device()
                if res:
                    print(_('Detect device is {0}').format(device_list[self.device_type]['name']))
                else:
                    print(_('Device is not {0}, please check it.').format(device_list[self.device_type]['name']))
                    raise Exception

        elif device_list[self.device_type]['protocol_version'] == 1:
            res, ver = self._cth.cmd_chk_protocol()
            if res and ver == 1:
                print(_('Confirm device is {0}').format(device_list[self.device_type]['name']))
            else:
                print(_('Device is not {0}, please check it.').format(device_list[self.device_type]['name']))
                raise Exception

        elif device_list[self.device_type]['protocol_version'] == 2:
            res, ver = self._cth.cmd_chk_protocol()
            if res and ver == 2:
                res, device_type = self._cth.cmd_v2_prog_chk_device()
                if res and device_type == self.device_type:
                    print(_('Confirm device is {0}').format(device_list[self.device_type]['name']))
                else:
                    print(_('Device is not {0}, please check it.').format(device_list[self.device_type]['name']))
                    raise Exception
            else:
                print(_('Device is not {0}, please check it.').format(device_list[self.device_type]['name']))
                raise Exception
        
        else:
            raise Exception
        
        self.protocol_version = device_list[self.device_type]['protocol_version']
    
    def _do_flash_prog_step(self):
        address = self.flash_pages[self.flash_page_index]['address']
        data    = self.flash_pages[self.flash_page_index]['data']
        if self.protocol_version == 1:
            self._cth.cmd_v1_flash_write(data)
            time.sleep(0.03)
        elif self.protocol_version == 2:
            if self.flash_page_index == 0:
                self._cth.cmd_v2_flash_earse_all()
            self._cth.cmd_v2_flash_write(address, data)
        
        self.flash_page_index += 1
        self.cur_step += 1
        if self.flash_page_index == len(self.flash_pages):
            self.status += 1

    def _do_eep_prog_step(self):
        if self.protocol_version == 2:
            self._cth.cmd_v2_eep_write(self.eep_pages[self.eep_page_index])

        self.eep_page_index += 1
        self.cur_step += 1
        if self.eep_page_index == len(self.eep_pages):
            self.status += 1

    def _do_prog_end(self):
        if self.protocol_version == 1:
            self._cth.cmd_v1_prog_end()
        elif self.protocol_version == 2:
            if self._is_go_app:
                self._cth.cmd_v2_prog_set_go_app_delay(self._go_app_delay)
                self._cth.cmd_v2_prog_end_and_go_app()
            else:
                self._cth.cmd_v2_prog_end()
        self.cur_step += 1

    def do_step(self):
        if self.status < len(self.st_list):
            if self.st_list[self.status] == self._State.FLASH_PROG:
                self._do_flash_prog_step()
            elif self.st_list[self.status] == self._State.EEP_PROG:
                self._do_eep_prog_step()
            elif self.st_list[self.status] == self._State.END:
                self._do_prog_end()
