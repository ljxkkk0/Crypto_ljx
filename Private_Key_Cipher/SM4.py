'''
SM4对称密码
支持ECB/CBC两种工作模式
'''
Sbox = \
    [
        0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05, 0x2B, 0x67,
        0x9A,
        0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99, 0x9C, 0x42, 0x50, 0xF4, 0x91,
        0xEF,
        0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62, 0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95,
        0x80,
        0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6, 0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C,
        0x19,
        0xE6, 0x85, 0x4F, 0xA8, 0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56,
        0x9D,
        0x35, 0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87, 0xD4,
        0x00,
        0x46, 0x57, 0x9F, 0xD3, 0x27, 0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E, 0xEA, 0xBF, 0x8A, 0xD2,
        0x40,
        0xC7, 0x38, 0xB5, 0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1, 0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A,
        0x55,
        0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3, 0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29,
        0x23,
        0xAB, 0x0D, 0x53, 0x4E, 0x6F, 0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A, 0x72, 0x6D,
        0x6C,
        0x5B, 0x51, 0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8,
        0x0A,
        0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8, 0xE5, 0xB4, 0xB0, 0x89, 0x69, 0x97,
        0x4A,
        0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84, 0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC,
        0x4D,
        0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48
    ]
CK = [0x00070E15, 0x1c232a31, 0x383f464d, 0x545b6269,
      0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
      0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
      0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
      0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
      0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
      0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
      0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]
FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]

SM4_ECB = 1
SM4_CBC = 2


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


def left_move(n, bit_len, move_step):  # 循环左移
    '''
    循坏左移
    :param n: 待处理数字n
    :param bit_len: n的比特长度
    :param move_step: 循环左移位数
    '''
    move_step = move_step % bit_len
    return ((n << move_step) & (2 ** bit_len - 1)) | (n >> (bit_len - move_step))


def cut_number(n, length, cnt):
    '''
    切分数字
    :param n: 待切分数字
    :param length: 切分后Bit长度
    :param cnt: 切分个数
    :return: 切分后数字数组
    '''
    num = []
    and_ = (1 << length) - 1
    while (cnt > 0):
        cnt -= 1
        num += [(n & and_)]
        n = n >> length
    num.reverse()
    return num


def glue_number(list, length):
    '''
    拼接数字
    :param list: 数组
    :param length: 每个数字的bit位数
    :return: 拼接后数字
    '''
    ans = 0
    for i in list:
        ans = (ans << length) | i
    return ans


class SM4_encrypt():
    '''
    SM4加密的类
    '''
    all_key = []

    def __init__(self, key, mode, IV=None):
        self.key = int((key), 16)
        self.mode = mode
        self.Iv = IV
        if mode not in [1, 2]:
            raise ValueError("Please choose the right mode!")

    def create_key(self):
        '''
        密钥生成
        :return: all_key[]
        '''
        num = cut_number(self.key, 32, 4)
        self.all_key = num[0:4] + [0] * 32
        for i in range(4):
            self.all_key[i] = (self.all_key[i] ^ FK[i])
        for round in range(32):
            K = self.all_key[round + 1] ^ self.all_key[round + 2] ^ self.all_key[round + 3]
            K = K ^ CK[round]
            num_ = cut_number(K, 8, 4)
            S = [0] * 4
            for i in range(4):
                S[i] = Sbox[num_[i]]
            K = glue_number(S, 8)
            K1 = left_move(K, 32, 13)
            K3 = left_move(K, 32, 23)
            K = K ^ K1 ^ K3
            self.all_key[round + 4] = self.all_key[round] ^ K
        self.all_key = self.all_key[4:]

    def one_group_encrypt(self, msg):
        '''
        分组加密函数
        :param msg: 待加密分组 int类型
        :return: 加密后密文 int类型
        '''
        init_X = cut_number(msg, 32, 4)
        X = init_X + [0] * 32
        for i in range(32):
            X = self.F(X, self.all_key, i)
        X.reverse()
        cipher = glue_number(X[0:4], 32)
        return cipher

    @staticmethod
    def F(X, rk, i):
        '''
        轮函数
        :param X: 轮输入
        :param rk: 轮密钥
        :param i: 当前轮数
        :return: 轮输出
        '''
        temp = X[i + 1] ^ X[i + 2] ^ X[i + 3]
        temp = temp ^ rk[i]
        num = cut_number(temp, 8, 4)
        after_Sbox = [0] * 4
        for j in range(4):
            after_Sbox[j] = Sbox[num[j]]
        temp = glue_number(after_Sbox, 8)
        temp_l1 = left_move(temp, 32, 2)
        temp_l2 = left_move(temp, 32, 10)
        temp_r1 = left_move(temp, 32, 18)
        temp_r2 = left_move(temp, 32, 24)
        temp = temp ^ temp_l1 ^ temp_l2 ^ temp_r1 ^ temp_r2
        temp = temp ^ X[i]
        X[i + 4] = temp
        return X

    @staticmethod
    def padding(s):
        """
        对消息进行PKCS#7填充
        """
        if not isinstance(s, str):
            raise ValueError("The input must be str type")
        length = len(s) // 2
        cnt = 16 - length % 16
        byte = hex(cnt)[2:].rjust(2, "0")
        return s + cnt * byte

    def mode_ecb(self, msg):
        '''
        ECB模式
        '''
        msg = self.padding(msg)
        self.create_key()
        cipher = ''
        length = len(msg)
        for i in range(length // 32):
            one_group = int(msg[i * 32:(i + 1) * 32], 16)
            cipher += hex(self.one_group_encrypt(one_group))[2:]
        return cipher

    def mode_cbc(self, msg):
        """
        CBC工作模式加密
        """
        msg = self.padding(msg)
        ciphertext = ""
        cipher_group = [self.Iv]
        length = len(msg)
        for i in range(length // 32):
            one_group = msg[i * 32:(i + 1) * 32]
            tmp = hex(int(one_group, 16) ^ int(cipher_group[i], 16))[2:].rjust(32, "0")
            tmp = int(tmp, 16)
            tmp = self.one_group_encrypt(tmp)
            tmp = hex(tmp)[2:]
            ciphertext += tmp
            cipher_group.append(tmp)
        return ciphertext

    def encrypt(self, msg):
        '''
        加密
        :param msg: 明文:bytes
        :return: 密文:bytes
        '''
        msg = bytes2hex(msg)
        self.create_key()
        ciphertext = ''
        if self.mode == SM4_ECB:
            ciphertext = self.mode_ecb(msg)
        elif self.mode == SM4_CBC:
            ciphertext = self.mode_cbc(msg)
        ciphertext = hex2bytes(ciphertext)
        return ciphertext


class SM4_decrypt():
    '''
    SM4解密的类
    '''
    all_key = []

    def __init__(self, key, mode, IV=None):
        self.key = int((key), 16)
        self.mode = mode
        self.Iv = IV
        if mode not in [1, 2]:
            raise ValueError("Please choose the right mode!")

    def create_key(self):
        '''
        密钥生成
        :return: all_key[]
        '''
        num = cut_number(self.key, 32, 4)
        self.all_key = num[0:4] + [0] * 32
        for i in range(4):
            self.all_key[i] = (self.all_key[i] ^ FK[i])
        for round in range(32):
            K = self.all_key[round + 1] ^ self.all_key[round + 2] ^ self.all_key[round + 3]
            K = K ^ CK[round]
            num_ = cut_number(K, 8, 4)
            S = [0] * 4
            for i in range(4):
                S[i] = Sbox[num_[i]]
            K = glue_number(S, 8)
            K1 = left_move(K, 32, 13)
            K3 = left_move(K, 32, 23)
            K = K ^ K1 ^ K3
            self.all_key[round + 4] = self.all_key[round] ^ K
        self.all_key = self.all_key[4:]
        self.all_key.reverse()

    def one_group_decrypt(self, msg):
        '''
        密文分组的解密
        :param msg: 待解密信息 int类型
        :return: 解密后信息   int类型
        '''
        init_X = cut_number(msg, 32, 4)
        X = init_X + [0] * 32
        for i in range(32):
            X = self.F(X, self.all_key, i)
        X.reverse()
        cipher = glue_number(X[0:4], 32)
        return cipher

    @staticmethod
    def F(X, rk, i):
        '''
        轮函数
        :param rk:轮密钥
        :param i:轮数
        '''
        temp = X[i + 1] ^ X[i + 2] ^ X[i + 3]
        temp = temp ^ rk[i]
        num = cut_number(temp, 8, 4)
        after_Sbox = [0] * 4
        for j in range(4):
            after_Sbox[j] = Sbox[num[j]]
        temp = glue_number(after_Sbox, 8)
        temp_l1 = left_move(temp, 32, 2)
        temp_l2 = left_move(temp, 32, 10)
        temp_r1 = left_move(temp, 32, 18)
        temp_r2 = left_move(temp, 32, 24)
        temp = temp ^ temp_l1 ^ temp_l2 ^ temp_r1 ^ temp_r2
        temp = temp ^ X[i]
        X[i + 4] = temp
        return X

    @staticmethod
    def remove_padding(s):
        """
        移除消息的填充
        """
        if not isinstance(s, str):
            raise ValueError("The input must be str type")
        byte = s[-2:]
        cnt = int(byte, 16)
        for i in range(cnt):
            s = s[:-2]
        return s

    def mode_ecb(self, cipher):
        """
        ECB工作模式解密
        """
        self.create_key()
        msg = ""
        length = len(cipher)
        for i in range(length // 32):
            one_group = int(cipher[i * 32:(i + 1) * 32], 16)
            ans = self.one_group_decrypt(one_group)
            ans = hex(ans)[2:]
            msg += ans
        msg = self.remove_padding(msg)
        return msg

    def mode_cbc(self, cipher):
        """
        CBC工作模式解密
        """
        msg = ""
        cipher_group = [self.Iv]
        length = len(cipher)
        for i in range(length // 32):
            one_group = cipher[i * 32:(i + 1) * 32]
            cipher_group.append(one_group)
            tmp = self.one_group_decrypt(int(one_group, 16))
            msg += hex(tmp ^ int(cipher_group[i], 16)).replace("0x", "").rjust(32, "0")
        msg = self.remove_padding(msg)
        return msg

    def decrypt(self, cipher):
        """
        对密文进行SM4解密
        """
        if not isinstance(cipher, bytes):
            return ValueError("The input must be bytes type")
        cipher = bytes2hex(cipher)
        self.create_key()
        plaintexe = ''
        if self.mode == SM4_ECB:
            plaintexe = self.mode_ecb(cipher)
        elif self.mode == SM4_CBC:
            plaintexe = self.mode_cbc(cipher)
        return hex2bytes(plaintexe)


def new(op, key, mode, Iv=None):
    """
    初始化一个SM4加密/解密对象
    :param op: 操作（加密/解密）
    :param key: 密钥 32位16进制字符
    :param mode: 选取工作模式
    :return: SM4加密/解密对象
    """
    if len(key) != 32:
        raise ValueError("The key must be 32 hexadecimal str numbers")
    elif op == "encrypt":
        return SM4_encrypt(key, mode, Iv)
    elif op == "decrypt":
        return SM4_decrypt(key, mode, Iv)
    else:
        raise ValueError("Wrong option you have chosen")


##测试代码
'''
import SM4
SM4en=SM4.new(op='encrypt',key='4046fb1985d94a7f1ff55ec7ec5f6054',mode=SM4.SM4_CBC,Iv='a8638d2fb23cc49206edd7c84532eaab')
msg=b'\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d'+b'\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d'
cipher=SM4en.encrypt(msg)
print(cipher)

SM4de=SM4.new(op='decrypt',key='4046fb1985d94a7f1ff55ec7ec5f6054',mode=SM4.SM4_CBC,Iv='a8638d2fb23cc49206edd7c84532eaab')
cipher=b'\xcb\xddV\x06B\x91\xb4j\x9b\xe2%\xc0\xd7^\\oF\xb6\xab\x91\xf2et\xb2bF\xe7W\x9e\xc2wb\xffsv\xa4\x83\xeb\xb3\x90\x95\xe8Z9\xa9?:\x99'
msg=SM4de.decrypt(cipher)
print(msg)
'''
