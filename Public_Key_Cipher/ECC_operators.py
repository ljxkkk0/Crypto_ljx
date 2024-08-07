from Math import Math

NULL_Point = [0, 0]
class Elliptic_Curve:
    def __init__(self, a, b, p, G=None, n=None):
        self.a = a
        self.b = b
        self.prime = p
        if 4 * a ** 3 + 27 * b ** 2 == 0:
            raise ValueError("The parameters (a,b) can't form an elliptic curve!")
        if not Math.is_prime(p):
            raise ValueError("The parameter p isn't a prime!")
        self.G = G
        self.n = n

    def add(self, P1, P2):
        '''
        两点之和
        :return: 两点相加得到的点
        '''
        P = self.prime
        a = self.a
        x1, y1 = P1
        x2, y2 = P2
        if self.is_opposite(P1, P2) == True:
            return NULL_Point
        if (x1 == x2) and (y1 == y2):
            k = ((3 * x1 * x1 + a) % P * (Math.Num_inv((2 * y1) % P, P))) % P
        else:
            k = ((y2 - y1) % P) * (Math.Num_inv((x2 - x1) % P, P)) % P
        x3 = (k ** 2 - x1 - x2) % P
        y3 = (k * (x1 - x3) - y1) % P
        return [x3, y3]

    def minus(self, P1, P2):
        '''
        两点之差
        '''
        P = [P2[0], -P2[1]]
        return self.add(P1, P)

    def multiply(self, P, k):
        '''
        点的倍乘
        :param P: 点
        :param k: 倍数
        '''
        list = []
        while (k > 0):
            list += [(k & 1)]
            k = k >> 1
        len_list = len(list)
        ans = P
        for i in range(len_list - 1, -1, -1):
            if (i != len_list - 1):
                ans = self.add(ans, ans)
                if (list[i] == 1):
                    ans = self.add(ans, P)
        return ans

    def is_null(self, Point):
        '''
        判断是否无穷远点
        :return: True/False
        '''
        return Point == NULL_Point

    def is_opposite(self, P1, P2):
        '''
        判断两个点是否是加法逆元
        :return: True/False
        '''
        x1, y1 = P1
        x2, y2 = P2
        if (x1 == x2) and ((y1 + y2) % self.prime == 0):
            return True
        return False

    def check_point(self, Point):
        """
        检查点是否在椭圆曲线上
        :return: True / False
        """
        if self.is_null(Point):
            return True
        x, y = Point
        left = (y ** 2) % self.prime
        right = ((x ** 3) % self.prime + self.a * x + self.b) % self.prime
        if left == right:
            return True
        return False
