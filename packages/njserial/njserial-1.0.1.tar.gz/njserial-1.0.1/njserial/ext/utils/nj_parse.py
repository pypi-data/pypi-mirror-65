from . import nj_re

'''
    数据转换模块
'''


def bytes_to_str(bs, encoding="utf-8"):
    '''
        byt转str
    :param bs:byt数据
    :param encoding:读取格式 base64,utf-8
    :return:转换后数据
    '''
    return bs.decode(encoding, 'strict')


def list_bytes_to_hexstr(bs):
    '''
        byt列表转16进制字符串
    :param bs:
    :return:
    '''
    value = ''
    for i in range(len(bs)):
        value += ''.join(['%02X ' % b for b in bs[i]])
    return value


def str_to_hexstr(str):
    '''
        字符串转16进制
    :param str:
    :return:
    '''
    return bytes.fromhex(str)


def hex_to_str(he):
    '''
        0x数据去掉0x
    :param he:16进制0xbc
    :return:去除0x
    '''
    by = nj_re.rm_to_str(str(he), filter='0x')
    if len(by) == 1:
        return "0" + by
    return by


def byt_to_hex(bi):
    '''
        bit转16进制字符串
    :param bi:要转换的bit位列表
    :return:
    '''
    try:
        if len(bi) > 0:  # 当列表为空时返回00
            sum = 0
            for i in bi:
                if i == 0:
                    sum += 1
                else:
                    sum += 2 ** i
            return hex_to_str(hex(sum))
        else:
            return "00"
    except Exception as err:
        print(err)


def data_replace_byt(data, bi):
    '''
        数据更换bit位
    :param data:初始数据
    :param bi:byt列表
    :return:转换后数据
    '''
    list1 = str_to_list(data, " ")
    for i in bi:
        if type(bi[i]) is list:
            list1[i - 1] = byt_to_hex(bi[i])
        else:
            list1[i - 1] = hex_to_str(hex(bi[i]))
    return str_add_space(list_to_str(list1))


def str_add_space(s):
    '''
        字符串+空格-->串口数据
    :param s:初始字符串
    :return:添加空格后字符串
    '''
    result = ''
    for i in range(len(s)):
        result += s[i]
        if i % 2 == 1:
            result += " "
    return result


def hex_to_bytlist(x):
    '''
        16进制转二进制列表
    :param x:16进制数据
    :return:二进制列表
    '''
    bytlist = []
    value = nj_re.rm_to_str(bin(int(x, 16)), "0b")
    for i in range(len(value)):
        if value[i] == '1':
            bytlist.append(len(value) - i)
    return bytlist


def hex_to_byt(cmd, position):
    '''
        16进制转二进制列表
    :param cmd:16进制数据
    :param position:解析位置
    :return:二进制列表
    '''
    return hex_to_bytlist(str_to_list(cmd)[position - 1])


def str_to_list(s, format=" "):
    '''
        字符串转列表
    :param s:初始字符串
    :param format:转换格式
    :return:转换后数据
    '''
    return s.split(format)


def list_to_str(list1):
    '''
        列表转成字符串
    :param list1:列表
    :return:字符串
    '''
    return ''.join(list1)


def checksum(cmd, formula=None, position=None, data_format='s'):
    '''
        效验位公式计算
    :param cmd:初步值
    :param formula:效验公式[BCC,CRC,CRC8,CRC16]
    :param position:效验位
    :param data_format:数据格式->默认小端s
    :return:效验后数据
    '''

    def list_add(value):
        if position == None:
            if len(value) > 2:
                if len(value) == 3:
                    value = "0{}".format(value)
                if data_format == 's':
                    list1.append(value[2:4])
                    list1.append(value[0:2])
                else:
                    list1.append(value[0:2])
                    list1.append(value[2:4])
            else:
                list1.append(value)
        else:
            if len(value) > 2:
                if len(value) == 3:
                    value = "0{}".format(value)
                if data_format == 's':
                    list1.insert(position - 1, value[2:4])
                    list1.insert(position, value[0:2])
                else:
                    list1.insert(position - 1, value[0:2])
                    list1.insert(position, value[2:4])
            else:
                list1.insert(position - 1, value)

    list1 = nj_re.rm_to_list(cmd)
    if formula == "BCC":
        list_add(hex_to_str(serial_crc.bcc(cmd)))
    elif formula == "CRC":
        list_add(hex_to_str(serial_crc.crc(cmd)))
    elif formula == "CRC8":
        list_add(hex_to_str(serial_crc.crc8(cmd)))
    elif formula == "CRC16":
        list_add(hex_to_str(serial_crc.crc16(cmd)))
    return str_add_space(list_to_str(list1))
