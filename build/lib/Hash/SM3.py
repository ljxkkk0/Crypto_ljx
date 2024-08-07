import os
from Math.Math import *
'''
SM3哈希函数
支持对文件进行Hash
'''

class SM3:
    digest_size = 256
    __IV = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]
    __text = b''
    __V_out = 0
    __T = []
    __W = []
    __W_ = []

    def __init__(self, plaintext=None):
        '''
        初始化函数
        :param plaintext: 输入字符串:bytes
        '''
        if not isinstance(plaintext, bytes):
            raise ValueError("The input must be a bytes")
        elif len(plaintext) > (1 << 61):
            raise IOError('The input is too long!')
        self.__text = self.padding(plaintext)
        self.init_T()
        len_bytes = len(self.__text)
        B_list = [int.from_bytes(self.__text[i:i + 64], 'big') for i in range(0, len_bytes, 64)]
        V = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
        for B in B_list:
            V = self.CV(V, B)

    def update(self, plaintext):
        if not isinstance(plaintext, bytes):
            raise ValueError("The input must be a bytes")
        elif len(plaintext) > (1 << 61):
            raise IOError('The input is too long!')
        self.__text = self.padding(plaintext)
        self.init_T()
        len_bytes = len(self.__text)
        B_list = [int.from_bytes(self.__text[i:i + 64], 'big') for i in range(0, len_bytes, 64)]
        V = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
        for B in B_list:
            V = self.CV(V, B)

    @staticmethod
    def padding(words_bytes):
        '''
        填充函数
        :param words_bytes: 待填充字符串
        :return: 填充后bytes串
        '''
        words_bitlen = len(words_bytes) * 8
        words_bytes += b'\x80'
        while (len(words_bytes) % 64) != 56:  # 56*8=448
            words_bytes += b'\x00'
        words_bytes += words_bitlen.to_bytes(8, 'big')
        return words_bytes

    @staticmethod
    def P0(X):
        return (X ^ left_move(X, 32, 9) ^ left_move(X, 32, 17))

    @staticmethod
    def P1(X):
        return (X ^ left_move(X, 32, 15) ^ left_move(X, 32, 23))

    @staticmethod
    def FF(j, X, Y, Z):
        '''
        布尔函数1
        :param j: 当前轮数
        '''
        if j < 16:
            return (X ^ Y ^ Z)
        elif j < 64:
            return ((X & Y) | (X & Z) | (Y & Z))
        else:
            return None

    @staticmethod
    def GG(j, X, Y, Z):
        '''
        布尔函数2
        :param j: 当前轮数
        '''
        if j < 16:
            return (X ^ Y ^ Z)
        elif j < 64:
            return ((X & Y) | ((~X) & Z))
        else:
            return None

    def init_T(self):
        '''
        初始化常量数组T
        '''
        T1 = [0x79cc4519 for i in range(0, 16)]
        T2 = [0x7a879d8a for i in range(16, 64)]
        self.__T = T1 + T2
        return self.__T

    def init_W(self, words_num):
        '''
        消息扩展函数
        :param words_num: 消息分组:int
        :return: W[68],W'[64]
        '''
        W = cut_number(words_num, 32, 16)
        for j in range(16, 68):
            num = self.P1((W[j - 16] ^ W[j - 9] ^ left_move(W[j - 3], 32, 15))) ^ left_move(W[j - 13], 32, 7) ^ W[j - 6]
            W += [num]
        W_ = [0] * 64
        for j in range(0, 64):
            W_[j] = W[j] ^ W[j + 4]
        return W, W_

    def CV(self, V_in, B_in):
        '''
        压缩函数
        '''
        [A, B, C, D, E, F, G, H] = cut_number(V_in, 32, 8)
        T = self.__T
        W, W_ = self.init_W(B_in)
        for j in range(0, 64):
            SS1 = left_move(((left_move(A, 32, 12) + E + left_move(T[j], 32, j)) & 0xffffffff), 32, 7)
            SS2 = SS1 ^ (left_move(A, 32, 12))
            TT1 = (self.FF(j, A, B, C) + D + SS2 + W_[j]) & 0xffffffff
            TT2 = (self.GG(j, E, F, G) + H + SS1 + W[j]) & 0xffffffff
            D = C
            C = left_move(B, 32, 9)
            B = A
            A = TT1
            H = G
            G = left_move(F, 32, 19)
            F = E
            E = self.P0(TT2)
        V_out = glue_number([A, B, C, D, E, F, G, H], 32)
        V_out = V_out ^ V_in
        self.__V_out = V_out
        return V_out

    def digest(self):
        '''
        输出字节类型
        '''
        return self.__V_out.to_bytes(256 // 8, 'big')

    def hexdigest(self):
        '''
        输出十六进制
        '''
        return hex(self.__V_out).rjust(256 // 4, '0')

    def file_hash(self, file_path: str) -> str:
        '''
        对文件的hash
        :param file_path: 文件路径
        :return: HASH值
        '''
        if not os.path.isfile(file_path):
            raise IOError('The file is not exsited')
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        self.update(plaintext)
        return self.hexdigest()
