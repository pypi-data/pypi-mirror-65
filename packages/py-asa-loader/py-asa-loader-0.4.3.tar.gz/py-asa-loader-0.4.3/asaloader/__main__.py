from asaloader.do_prog import do_prog
from asaloader.device import device_list
from asaloader.ihex import isIHex
from asaloader.locale import _

import argparse
import os
import sys
import serial.tools.list_ports
import gettext

"""list: 副命令 prog 的參數資訊描述
用來作為 ArgumentParser.add_argument 的參數。

若直接使用 ArgumentParser.add_argument 來新增參數，會有非常多行，
且參數較難管理，所以參數資訊集中存放在此變數中，待 ArgumentParser
在初始化時，在去切割此變數，拿出各個參數的資訊。
"""
_cmd_prog_args = [
    {
        'name': ('-d', '--decice'),
        'opts': {
            'action': 'store',
            'dest': 'device',
            'type': str,
            'default': 'auto',
            'help': _('The name or number of the device type to be programmed. Can see available device type by subcommand print-device-list.'),
        }
    },
    {
        'name': ('-p', '--port'),
        'opts': {
            'action': 'store',
            'dest': 'port',
            'type': str,
            'required': True,
            'help': _('The serial port which program burn the device.'),
        }
    },
    {
        'name': ('-f', '--flash'),
        'opts': {
            'action': 'store',
            'dest': 'flash_file',
            'type': str,
            'required': False,
            'help': _('Set binary file which program to flash.'),
        }
    },
    {
        'name': ('--fm', '--flash-memory'),
        'opts': {
            'action': 'store',
            'dest': 'flash_mem',
            'type': int,
            'required': False,
            'help': _('Set program start memory location in flash. If flash_format is \'ihex\', this parameter is ignored. Default is 0. (future work, not availabe now)'),
        }
    },
    {
        'name': ('--ff', '--flash-format'),
        'opts': {
            'action': 'store',
            'dest': 'flash_format',
            'type': str,
            'required': False,
            'default': 'ihex',
            'help': _('Set the flash binary file format, default is \'ihex\'. (only ihex now)'),
        }
    },
    {
        'name': ('-e', '--eeprom'),
        'opts': {
            'action': 'store',
            'dest': 'eep_file',
            'type': str,
            'required': False,
            'help': _('Set binary file which write to eeprom.'),
        }
    },
    {
        'name': ('--em', '--eeprom-memory'),
        'opts': {
            'action': 'store',
            'dest': 'eep_mem',
            'type': int,
            'required': False,
            'help': _('Set data start memory location eeprom flash. If eep_format is \'ihex\', this parameter is ignored. Default is 0. (future work, not availabe now)'),
        }
    },
    {
        'name': ('--ef', '--eeprom-format'),
        'opts': {
            'action': 'store',
            'dest': 'eep_format',
            'type': str,
            'required': False,
            'default': 'ihex',
            'help': _('Set the eeprom binary file format, default is \'ihex\'. (only ihex now)'),
        }
    },
    {
        'name': ('-a', '--after-prog-go-app'),
        'opts': {
            'action': 'store_true',
            'dest': 'is_go_app',
            'required': False,
            'help': _('Enter the application after programing.'),
        }
    },
    {
        'name': ('-D', '--go-app-delay'),
        'opts': {
            'action': 'store',
            'dest': 'go_app_delay',
            'type': int,
            'required': False,
            'default': 50,
            'help': _('Set delay time from programing complete to enter application, in ms.'),
        }
    }
]


def prog_args_handler(args):
    args.device_type = check_arg_device(args.device)
    args.is_prog_eep = False
    args.is_prog_flash = False

    if (args.flash_file is None) and (args.eep_file is None):
        print(_('Error: No flash or eeprom needs to be burned, please use \'-f \', \'-e \' to specify the file to be burned.'))
        sys.exit(1)

    if args.flash_file is not None:
        args.is_prog_flash = True

        if not os.path.isfile(args.flash_file):
            print('Error: Cannot find flash binary file {0}.'.format(
                args.flash_file))
            sys.exit(1)
        elif not isIHex(args.flash_file):
            print('Error: The flash binary file {0} is not ihex formatted.'.format(
                args.flash_file))
            sys.exit(1)

    if args.eep_file is not None:
        args.is_prog_eep = True

        if not os.path.isfile(args.eep_file):
            print(_('Error: Cannot find eeprom binary file {0}.').format(
                args.eep_file))
            sys.exit(1)
        elif not isIHex(args.eep_file):
            print(_('Error: The eeprom binary file {0} is not ihex formatted.').format(
                args.eep_file))
            sys.exit(1)

    if args.port not in [p[0] for p in serial.tools.list_ports.comports()]:
        print(_('Error: Cannot find serial port {0}.').format(args.port))
        print(_('The available serial ports are as follows:'))
        print_ports()
        sys.exit(1)

    if args.flash_mem is not None:
        print(_('Error: --flash-mem is not supported in current verison.'))
        sys.exit(1)

    if args.eep_mem is not None:
        print(_('Error: --eeprom-mem is not supported in current verison.'))
        sys.exit(1)

    if args.flash_format is not 'ihex':
        print(_('Error: Parameter --flash-format is illegal.'))
        print(_('Available parameters:'))
        print(_('   ihex:    intel hex formatted'))
        sys.exit(1)

    if args.eep_format is not 'ihex':
        print(_('Error: Parameter --eeprom-format is illegal.'))
        print(_('Available parameters:'))
        print(_('   ihex:    intel hex formatted'))
        sys.exit(1)

    return args


def print_device_list():
    s = _("Available device list:\n")
    s += _("    device name   \t num \t note\n")
    for dev in device_list:
        s += "  - {0:11s}  \t {1:4s}\t {2}\n".format(
            dev['name'], str(dev['dev_type']), dev['note'])

    print(s)


def print_ports():
    for (port, desc, hwid) in serial.tools.list_ports.comports():
        print("{:20}".format(port))
        print("    desc: {}".format(desc))
        print("    hwid: {}".format(hwid))


def check_arg_device(dev):
    if dev.isdigit():
        for device in device_list:
            if int(dev) == device['dev_type']:
                return device['dev_type']
    else:
        for device in device_list:
            if dev == device['name']:
                return device['dev_type']

    print(_('Error: Parameter --device is illegal.'))
    print_device_list()
    sys.exit(1)


def parser_init(parser):
    parser.description = _('Program to ASA-series board.')
    parser.add_argument(
        '--lc',
        action='store',
        dest='lc',
        type=str,
        required=False,
        default='',
        help=_('Set the language code. e.g. `zh_TW`, `en_US`')
    )

    subparsers = parser.add_subparsers(dest='subcmd')
    parser_prog = subparsers.add_parser(
        'prog', help=_('Program code to board.'))

    subparsers.add_parser('print-device-list',
                          help=_('List all available devices.'))
    subparsers.add_parser(
        'print-ports', help=_('List all available serial ports.'))

    for arg in _cmd_prog_args:
        parser_prog.add_argument(*arg['name'], **arg['opts'])


def run():
    parser = argparse.ArgumentParser()
    parser_init(parser)
    args = parser.parse_args()

    if args.subcmd == 'print-device-list':
        print_device_list()
    elif args.subcmd == 'print-ports':
        print_ports()
    elif args.subcmd == 'prog':
        args = prog_args_handler(args)
        do_prog(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    run()
