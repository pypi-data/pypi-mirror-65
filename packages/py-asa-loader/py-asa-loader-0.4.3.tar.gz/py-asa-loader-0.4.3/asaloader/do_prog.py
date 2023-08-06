from asaloader.ihex import parseIHex
from asaloader.loader import Loader
from asaloader.device import device_list
from asaloader.locale import _

import progressbar
import serial
import sys
import time
import math

def do_prog(args):

    ser = serial.Serial()
    ser.port = args.port
    ser.baudrate = 115200
    ser.timeout = 1
    try:
        ser.open()
    except:
        print(_('ERROR: com port has been opened by another application.').format(args.port))
        sys.exit(1)
    
    loader = Loader(ser, args)

    # print('flash  花費大小為 {0:0.2f} KB ({1} bytes) 。'.format(len(flash_data)/1024, len(flash_data)))
    # print('eeprom 花費大小為 {0} bytes。'.format(len(eep_data)))

    # cost_t = math.ceil(len(flash_data)/256) * 0.047 + math.ceil(len(eep_data)/256) * 0.05 + 0.23
    # print('預估花費時間為 {0} s。'.format(cost_t))

    widgets=[
        ' [', progressbar.Timer(_('Elapsed Time: %(seconds)s s'), ), '] ',
        progressbar.Bar(),
        progressbar.Counter(format='%(percentage)0.2f%%'),
    ]
    
    bar = progressbar.ProgressBar(max_value=loader.total_steps, widgets=widgets)
    bar.update(0)
    for i in range(loader.total_steps):
        try:
            loader.do_step()
            bar.update(i)
        except:
            bar.finish(end='\n', dirty=True)
            raise Exception
