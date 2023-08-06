import conftest
from asaprog import pac_encode
from asaprog.pac_const import *


if __name__ == "__main__":
    pac = {
        'command': Command.CHK_DEVICE.value,
        'data': b'test'
    }
    res = pac_encode(pac)
    print(res)
    print(res[-1])
