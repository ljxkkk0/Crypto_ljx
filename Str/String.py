def s2n(s):
    '''
    字符串转化为数字
    仅接受'str'以及'bytes'类型字串
    采用'utf-8'编码
    返回大端存储的数字
    :param s: 字符
    :return:
    '''
    if type(s) == type(''):
        b = s.encode('utf-8')
        num = int.from_bytes(b, "big")
        return num
    elif type(s) == type(b''):
        num = int.from_bytes(s, "big")
        return num
    else:
        raise TypeError("TypeError: it should be 'str' or 'bytes'")


def n2s(num):
    '''
    数字转化为’utf-8‘编码字符串
    大端存储
    :param num: 待转化的数字
    :return: 'utf-8'字符串
    '''
    bit_len = num.bit_length()
    byte_len = (bit_len + 7) >> 3
    return num.to_bytes(byte_len, 'big')


def bytes2hex(b):
    """
    字节串转16进制
    """
    s = ""
    for byte in b:
        s += hex(byte)[2:].rjust(2, "0")
    return s


def hex2bytes(h):
    """
    16进制转字节串
    采用大端存储
    """
    length = len(h)
    if length & 1 == 1:
        length += 1
    return int(h, 16).to_bytes(length // 2, 'big')
