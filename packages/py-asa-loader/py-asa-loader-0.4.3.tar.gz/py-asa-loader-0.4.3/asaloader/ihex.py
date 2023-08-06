# intel hex can vew its spec at http://www.interlog.com/~speff/usefulinfo/Hexfrmt.pdf
# 
def parseIHex(filename):
    """parse a intel style hex to raw binary data"""
    # todo sort
    with open(filename, 'r') as hexfile:
        s_i = 0 # sections index
        sections = []
        ext_addr = 0

        for line in hexfile.readlines():
            try:
                length = int(line[1:3], 16)
                address = int(line[3:7], 16)
                content_type = int(line[7:9], 16)
                if length != 0:
                    data = bytearray.fromhex(line[9: 9 + length*2])
                else:
                    data = b''
            
            except:
                raise Exception("Invalid hexfile!", filename)

            if content_type == 0:
                if s_i == 0:
                    sections += [{
                        'address': (ext_addr << 16) + address,
                        'data': data
                    }]
                    s_i = s_i + 1
                elif (
                    (ext_addr << 16) + address ==
                    sections[s_i-1]['address'] + len(sections[s_i-1]['data'])
                ):
                    sections[s_i-1]['data'] = sections[s_i-1]['data'] + data
                else:
                    sections += [{
                        'address': (ext_addr << 16) + address,
                        'data': data
                    }]
                    s_i = s_i + 1
            elif content_type == 1:
                # End Of File
                if address == 0:
                    break
                else:
                    raise Exception("Invalid hexfile!", filename)
            elif content_type == 2:
                # Extended Segment Address
                pass
            elif content_type == 3:
                # Start Segment Address
                pass
            elif content_type == 4:
                # Extended Linear Address
                ext_addr = address
                pass
            elif content_type == 5:
                # Start Linear Address
                pass

    return sections

def resize_to_page(h, pgsz):
    res = []
    for sect in h:
        sect_addr = sect['address']
        sect_data = sect['data']

        # 起始位置若不在 pgsz * N 上
        # 往前補 0xFF
        if sect_addr % pgsz != 0:
            n = sect_addr // pgsz
            l = sect_addr - pgsz * n
            sect_addr = pgsz * n
            a = bytes([0xff for i in range(l)])
            sect_data = a + sect_data
        
        # 結束位置 + 1 若不在 pgsz * N 上
        # 往後補 0xFF
        if (sect_addr + len(sect_data)) % pgsz != 0:
            n = (sect_addr + len(sect_data)) // pgsz
            l = pgsz * (n + 1) - (sect_addr + len(sect_data))
            a = bytes([0xff for i in range(l)])
            sect_data = sect_data + a

        res += [{
            'address': sect_addr,
            'data': sect_data
        }]
    
    return res
        
def cut_to_pages(h, pgsz):
    res = []
    for sect in h:
        sect_addr = sect['address']
        sect_data = sect['data']
        for i in range(len(sect_data)//pgsz):
            res += [{
                'address': sect_addr + i * pgsz,
                'data': sect_data[i * pgsz : i * pgsz + pgsz]
            }]
    return res


def isIHex(filename):
    try:
        parseIHex(filename)
    except:
        return False
    return True
