import random

# 常数定义
e = 2.718281828459045
pi = 3.141592653589793
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                991, 997]


# 常用函数
def Euclidean(a, b):
    '''
    括展欧几里得算法
    求解x*a+y*b=gcd
    :param a: 参数a
    :param b: 参数b
    :return: 式子中的x,y,gcd
    '''
    if b == 0:
        return 1, 0, a
    else:
        x, y, gcd = Euclidean(b, a % b)  # 递归直至余数等于0(需多递归一层用来判断)
        x, y = y, (x - (a // b) * y)  # 辗转相除法反向推导每层a、b的因子使得gcd(a,b)=ax+by成立
        return x, y, gcd


def Quickmod(a, b, m):
    '''
    快速模幂
    :param a: 底数
    :param b: 指数
    :param m: 模数
    '''
    ans = 1
    while (b > 0):
        if (b % 2 == 1):
            ans = (ans * a) % m
        b = b >> 1
        a = (a * a) % m
    return ans


def left_move(n, bit, move_step):
    '''
    循环左移
    :param n: 数据
    :param bit: 数据的bit长度
    :param move_step: 循环左移位数
    '''
    move_step = move_step % bit
    return ((n << move_step) & (2 ** bit - 1)) | (n >> (bit - move_step))


def Num_inv(a, m):
    '''
    求解a模m下的逆
    :param a: 参数1
    :param m: 参数2
    :return: a mod m 的最小正逆元
    '''
    inv, _, gcd = Euclidean(a, m)
    if gcd != 1:
        raise ValueError("The input numbers aren't coprime！")
    else:
        inv = inv % m
        return inv


def miller_rabin(num):
    '''
    MillerRabin素性检测
    若 10 次随机选取的数均不是num是合数的证据，则认为num是素数
    :param num: 待测试数
    :return: True/False-> True:num is prime;False:num is not prime
    '''
    s = num - 1
    k = 0
    while s % 2 == 0:
        s = s >> 1
        k += 1
    for try_time in range(10):  # 随机选try_time个数试验 ，这里都选十个数
        a = random.randrange(2, num - 1)
        v = Quickmod(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == k - 1:
                    return False
                else:
                    i = i + 1
                    v = (v * v) % num
    return True


def is_prime(num):  # 判断输入数据是否是素数
    '''
    质数判定算法
    结合小整数质数表和米勒拉宾素性检测判断num是否是素数
    :param num: 待判定的数
    :return: True/False-> True:num is prime;False:num is not prime
    '''
    global small_primes
    if num < 2:  # 排除0,1和负数
        return False  # 较小素数生成表，加快素数判定
    if num in small_primes:  # 在小素数表中
        return True
    for prime in small_primes:  # 是否可以被小素数整除，可整除即是合数
        if num % prime == 0:
            return False  # 如果这样没有分辨出来,就一定是大整数,那么就调用rabin算法
    return miller_rabin(num)


def get_prime(bit_size):
    '''
    大素数生成算法
    输出 bit_size 位长的素数
    :param bit_size: 素数的bit长度
    '''
    while True:
        num = random.randrange((1 << (bit_size - 1)), (1 << (bit_size + 1)))
        if is_prime(num):
            return num


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


def upper_num(n):
    '''
    上取整
    :param n: 待计算数字
    :return:  上取整结果
    '''
    if int(n) < n:
        return int(n + 1)
    else:
        return int(n)


def lower_num(n):
    '''
    下取整
    '''
    return int(n)


def num_bytesize(n):  # 返回n的字节长度
    n = format(n, 'b')
    size = upper_num(len(n) / 8)
    return size
