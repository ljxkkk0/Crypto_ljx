from Public_Key_Cipher import ECC_operators, SM2
from Math import Math
from Str.String import s2n, n2s, bytes2hex, hex2bytes
from Hash.SM3 import SM3


hash_algorithm = SM3

class Sign_And_Verify:
    Pk: list
    __d: int
    __Z: bytes
    __k: int

    def __init__(self, a, b, prime, G, n, ID, Pk=None, d=None, k=None):
        e = ECC_operators.Elliptic_Curve(a, b, prime, G, n)
        if e.check_point(G) == False:
            raise ValueError("Invalid parameter G")
        if not isinstance(ID, bytes):
            raise ValueError("Invalid parameter ID ! Bytes needed!")
        if not Math.is_prime(prime):
            raise ValueError("Invalid parameter prime!")
        self.Curve = ECC_operators.Elliptic_Curve(a=a, b=b, p=prime, G=G, n=n)
        self.ID = ID
        self.Pk = Pk
        self.__d = d
        self.__k = k
        self.get_Z()

    def get_Z(self):
        ENTL: bytes = (len(self.ID) * 8).to_bytes(2, 'big')
        a_bytes = n2s(self.Curve.a)
        b_bytes = n2s(self.Curve.b)
        G_x_bytes = n2s(self.Curve.G[0])
        G_y_bytes = n2s(self.Curve.G[1])
        Pk_x_bytes = n2s(self.Pk[0])
        Pk_y_bytes = n2s(self.Pk[1])
        hash_input = ENTL + self.ID + a_bytes + b_bytes + G_x_bytes + G_y_bytes + Pk_x_bytes + Pk_y_bytes
        self.Z = hash_algorithm(hash_input).digest()
        return self.Z

    def Sign(self, Message):
        if not isinstance(Message, bytes):
            raise ValueError("The message should be bytes!")
        Z = self.Z
        M_ = Z + Message
        e = int.from_bytes(hash_algorithm(M_).digest(), 'big')
        G1 = self.Curve.multiply(self.Curve.G, self.__k)
        x1, y1 = G1
        r = (e + x1) % self.Curve.n
        s = Math.Num_inv(1 + self.__d, self.Curve.n) * (self.__k - r * self.__d) % self.Curve.n
        return (r, s)

    def Verify(self, Message, r, s):
        n = self.Curve.n
        add = self.Curve.add
        multi = self.Curve.multiply
        G = self.Curve.G
        if not isinstance(Message, bytes):
            raise ValueError("The message should be bytes!")
        if r > n - 1 or r < 1 or s > n - 1 or s < 1:
            raise ValueError("The signature is WRONG!")
        Z = self.get_Z()
        M_ = Z + Message
        e = int.from_bytes(hash_algorithm(M_).digest(), 'big')
        t = (r + s) % n
        if t == 0:
            raise ValueError("The signature is WRONG!")
        Point = add(multi(G, s), multi(self.Pk, t))
        v = (e + Point[0]) % n
        if v == r:
            return True
        else:
            return False


def new(Mode, a, b, prime, G, n, ID, Message, Pk=None, d=None, k=None, r=None, s=None):
    DEMO = Sign_And_Verify(a=a, b=b, prime=prime, G=G, ID=ID, Pk=Pk, d=d, k=k, n=n)
    if Mode == "Sign":
        return DEMO.Sign(Message)
    elif Mode == "Verify":
        return DEMO.Verify(Message, r, s)
    else:
        raise ValueError("Mode should be ‘Sign’ or 'Verify' !")
