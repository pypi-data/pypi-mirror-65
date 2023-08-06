import enum

HEADER = b'\xFC\xFC\xFC'
TOCKEN = b'\x01'


class Command(enum.IntEnum):
    # for both version 1 and version 2
    CHK_PROTOCOL = 0xFA

    # for version 1 protocol supproted device such as
    #   asa_m128_v1
    #   asa_m128_v2
    ACK1 = 0xFB
    DATA = 0xFC
    ACK2 = 0xFD

    # for version 2 protocol supproted device such as
    #   asa_m128_v3
    #   asa_m3_v1
    PROG_CHK_DEVICE         = 0x02
    PROG_END                = 0x03
    PROG_END_AND_GO_APP     = 0x04
    PROG_SET_GO_APP_DELAY   = 0x05

    FLASH_SET_PGSZ      = 0x10
    FLASH_GET_PGSZ      = 0x11
    FLASH_WRITE         = 0x12
    FLASH_READ          = 0x13
    FLASH_VARIFY        = 0x14
    FLASH_EARSE_SECTOR  = 0x15
    FLASH_EARSE_ALL     = 0x16

    EEPROM_SET_PGSZ     = 0x20
    EEPROM_GET_PGSZ     = 0x21
    EEPROM_WRITE        = 0x22
    EEPROM_READ         = 0x23
    EEPROM_EARSE        = 0x24
    EEPROM_EARSE_ALL    = 0x25
