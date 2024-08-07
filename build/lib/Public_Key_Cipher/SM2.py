from Hash import SM3
from random import randint
from Math import Math
from Public_Key_Cipher import ECC_operators



hash_algorithm = SM3.SM3
hLen = hash_algorithm.digest_size * 8


def KDF(Z, klen):
    '''
    SM2密钥派生函数KDF
    '''
    ct = 0x00000001
    upper = Math.upper_num((klen / hLen))
    bytes_len = klen // 8
    Hash = b''
    for i in range(1, upper + 1):
        byte = ((Z) + ct.to_bytes(4, 'big'))
        hash_value = hash_algorithm(byte).digest()
        Hash += hash_value
        ct += 1
    ans = Hash[:bytes_len]
    return int.from_bytes(ans, 'big')


class SM2:
    __k: int
    __PB: list

    def __init__(self, a, b, prime, G, n=None, Par=None):
        '''
        初始化参数
        :param a: 椭圆曲线参数a
        :param b: 椭圆曲线参数b
        :param prime: 大素数
        :param G: 基点
        :param n: 椭圆曲线的阶
        :param Par: 参数长度
        '''
        self.curve = ECC_operators.Elliptic_Curve(a, b, prime, G, n)
        self.init_Par(prime)
        if Par != None:
            self.Par = Par
        self.G = G

    def init_Par(self, prime):
        '''
        初始化参数长度
        :param prime: 选用的大素数
        :return: 大素数的bit长度
        '''
        len_ = Math.num_bytesize(prime)
        self.Par = len_ * 8

    def init_Key(self, k=None, PB=None, d=None):
        '''
        初始化密钥/随机数
        :param k: 加密使用的随机数
        :param PB: 公钥
        :param d: 私钥
        '''
        self.k = k
        self.PB = PB
        self.d = d

    def encrypt(self, plaintext: bytes):
        '''
        SM2加密函数
        :param plaintext: 明文:bytes
        :return: 密文:str
        '''
        if not isinstance(plaintext, bytes):
            raise ValueError("The plaintext should be bytes")
        ECC = self.curve
        C1 = ECC.multiply(self.G, self.k)
        C = ECC.multiply(self.PB, self.k)
        x2, y2 = C
        x2_bytes = x2.to_bytes(self.Par // 8, 'big')
        y2_bytes = y2.to_bytes(self.Par // 8, 'big')
        klen = len(plaintext) * 8
        t = KDF(x2_bytes + y2_bytes, klen)
        M = int.from_bytes(plaintext, 'big')
        C2 = M ^ t
        Hash_input = x2_bytes + plaintext + y2_bytes
        C3 = hash_algorithm(Hash_input).digest()
        C3 = int.from_bytes(C3, 'big')
        Cipher = ("0x04" + "%0*x" % (self.Par // 4, C1[0]) + "%0*x" % (self.Par // 4, C1[1]) + "%0*x" % (
            klen // 4, C2) + "%0*x" % (hLen // 4, C3))
        return Cipher

    def decrypt(self, Cipher):
        '''
        SM2解密函数
        :param Cipher: 密文:str
        :return: 明文:bytes
        '''
        if not isinstance(Cipher, str):
            raise ValueError("The cipher text should be a hexadecimal string!")
        Cipher = Cipher.replace('0x', '')
        Cipher_len = len(Cipher) * 4
        Cipher_num = int(Cipher, 16)
        klen = Cipher_len - (8 + 2 * self.Par + hLen)
        C1 = (Cipher_num >> (Cipher_len - 8 - 2 * self.Par))
        C2 = (Cipher_num >> hLen) & (2 ** klen - 1)
        y1 = C1 & (2 ** self.Par - 1)
        x1 = (C1 >> self.Par) & (2 ** self.Par - 1)
        C = [x1, y1]
        x2, y2 = self.curve.multiply(C, self.d)
        x2_byte = x2.to_bytes(self.Par // 8, 'big')
        y2_byte = y2.to_bytes(self.Par // 8, 'big')
        t = KDF(x2_byte + y2_byte, klen)
        M_ = C2 ^ t
        Plaintext = M_.to_bytes(klen // 8, 'big')
        return Plaintext


def new(a, b, prime, G, n, Par=None):
    sm2 = SM2(a, b, prime, G, Par=Par)
    Pb, d, k = key_generate(prime, a, b, G, n)
    sm2.init_Key(k, Pb, d)
    return sm2


def key_generate(prime, a, b, G, n):
    """
    SM2密钥生成函数
    """
    d = randint(1, n - 1)  # 私钥
    k = randint(1, n - 1)  # 加密随机数
    ECC = ECC_operators.Elliptic_Curve(a, b, prime)
    Pb = ECC.multiply(G, d)  # 生成公钥
    return Pb, d, k
