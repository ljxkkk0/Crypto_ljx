## MyCrypto使用介绍
### 1. Math模块

该模块包含了密码学中的很多常用数学运算，如快速模幂、求逆、生成大素数、括欧算法等。

- Math.py

    - Euclidean(a,b)

        扩展欧几里得算法，用于求解裴蜀定理中的系数，使用方法如下

        `x, y, gcd = Euclidean(a, b) # 其中g=(a, b)，xa+yb=gcd`
        
    - Quickmod(a,b,m)

        快速模幂算法，a为底数，b为指数，m为模数，使用方法如下

        `sum = Quickmod(a,b,m) `
    
    - left_move(n,bit_len,move_step)
        
        循环左移，参数说明见注释，使用方法如下

        `n=left_move(n,length,step)`
    
    - Num_inv(a,m)

        求逆元，求a mod m的逆元，使用方法如下

        `inv = Num_inv(a,m)#满足 (inv*a)%m=1 `
    
    - miller_rabin(num)
        
        米勒拉宾素性检测，默认检测十次，使用方法如下
    
        `miller_rabin(num)#return True/False`
    - is_prime(num)
      
        素数判断算法，小数据时结合素数表直接判断，大数据时调用miller_rabin素性检测算法，使用方法如下
    
        `is_prime(num)#return True/False`
    
    - is_prime(num)
      
        素数判断算法，小数据时结合素数表直接判断，大数据时调用miller_rabin素性检测算法，使用方法如下
    
        `is_prime(num)#return True/False`  
      
    - cut_number(n,unit_length,cnt)
    
        切分数字，将n切分成cnt个unit_length长度的数字，不足则高位补零，使用方法如下  
        
        `list = cut_number(n,32,4)#将n切分成5个32位的数字 `
    
    - glue_number(list,length)
    
        拼接数字，将list中数字按大端存储的顺序拼接成新的数字，length为单个数字比特长度，使用方法如下
    
        `num = glue_number(num_list,unit_len)`
    
### 2. Str模块
- String.py

    - s2n

        将一个字符串s(str/bytes)转成一个整数(int)，使用方法如下

        `n = s2n(s)`

    - n2s

        将一个整数n(int)转化成一个字节串(bytes)，使用方法如下

        `b = n2s(n)`
    
    - bytes2hex
    
        字节串(bytes)转为16进制(str),高位补零，使用方法如下
    
        `h = bytes2hex(b)`  
      
    - hex2bytes
      
        16进制(str)转字节串(bytes)，大端存储，使用方法如下
    
        `b = hex2bytes(h)`
    

### 3. Private_Key_Cipher模块

该模块为对称密码，包含sM4分组密码算法，支持ECB、CBC两种工作模式进行加密/解密

- SM4.py

    - 该文件包含两个类SM4_encrypt、SM4_decrypt，分别用于加密、解密；

    - 包含两个参数SM4_ECB、SM4_CBC，分别代表ECB工作模式、CBC工作模式

    - 包含一个函数new，用于创建加密/解密对象

  具体使用方法如下所示：

  - ECB模式：

    ```python
    from Private_Key_Cipher import SM4
    """
    op取值'encrypt'或'decrypt'，代表加密或解密 :str
    key为密钥 (16进制):str
    mode为选取的工作模式，取值为SM4.SM4_ECB或SM4_CBC
    Iv为CBC模式中所用的初始向量，可为空
    """
    #SM4_ECB测试
    SM4en=SM4.new(op='encrypt',key='4046fb1985d94a7f1ff55ec7ec5f6054',mode=SM4.SM4_ECB,Iv='a8638d2fb23cc49206edd7c84532eaab')
    msg1=b'\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d'+b'\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d'
    cipher=SM4en.encrypt(msg)
    print(cipher)
    '''
    cipher=b'"\xec\xa9}\xcb2\x10\x17\xd0\xa0Y)h\xf1\xe5?"\xec\xa9}\xcb2\x10\x17\xd0\xa0Y)h\xf1\xe5?\xbcGX\xe1\xa3i\x13\x06m\xb6\xce\xdc\xe6\x1fz7'
    '''
    
    SM4de=SM4.new(op='decrypt',key='4046fb1985d94a7f1ff55ec7ec5f6054',mode=SM4.SM4_ECB,Iv='a8638d2fb23cc49206edd7c84532eaab')
    msg2=SM4de.decrypt(cipher)
    print(msg)
    '''
    msg2=b'\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d'
    '''
    print(msg1 == msg2)
    # True

  

		
   - CBC模式：

    ```python
    #SM4_CBC测试
    from Private_Key_Cipher import SM4
    SM4en=SM4.new(op='encrypt',key='4046fb1985d94a7f1ff55ec7ec5f6054',mode=SM4.SM4_CBC,Iv='a8638d2fb23cc49206edd7c84532eaab')
    msg1=b'\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d'+b'\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d'
    cipher=SM4en.encrypt(msg)
    print(cipher)
    '''
    cipher=b'\xcb\xddV\x06B\x91\xb4j\x9b\xe2%\xc0\xd7^\\oF\xb6\xab\x91\xf2et\xb2bF\xe7W\x9e\xc2wb\xffsv\xa4\x83\xeb\xb3\x90\x95\xe8Z9\xa9?:\x99'
    '''
    
    SM4de=SM4.new(op='decrypt',key='4046fb1985d94a7f1ff55ec7ec5f6054',mode=SM4.SM4_CBC,Iv='a8638d2fb23cc49206edd7c84532eaab')
    msg2=SM4de.decrypt(cipher)
    print(msg2)
    '''
    msg2=b'\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d\xc0J\x9b1\x1a/\xc2E\xf7B\xc5q\x9f\xcf$\x9d'
    msg1==msg2
    '''
    
    



### 4. Public_Key_Cipher模块

该非对称密码模块，包含了椭圆曲线基本操作以及基于椭圆曲线的SM2公钥加密/解密

- ECC_operators.py

    椭圆曲线模块，用于实现椭圆曲线上的基本运算

    - 包含一个参数NULL_Point，表示椭圆曲线上的无穷远点
    - 包含一个类Elliptic_Curve，用于根据初始参数实例化一个椭圆曲线对象，可实现加法、减法、数乘等方法以及判断点是否在曲线上。

  具体使用方法如下所示：

    ```python
    from Public_Key_Cipher import ECC_operators
    a=115792089210356248756420345214020892766250353991924191454421193933289684991996
    b=18505919022281880113072981827955639221458448578012075254857346196103069175443
    p=115792089210356248756420345214020892766250353991924191454421193933289684991999
    Point1 = [64901889550129866513443884082574452575157116031103742365434905633820925813192,
          84553412528427919723206133858954594911213526647800598970633596412071681640913]
    Point2= [64901889550129866513443884082574452575157116031103742365434905633820925813192,
          84553412528427919723206133858954594911213526647800598970633596412071681640913]
    
    Curve_demo=ECC_operators.Elliptic_Curve(a=a,b=b,p=p)
    
    Point3=Curve_demo.add(Point2,Point1)
    print(Point3)
    #输出：[91829719240076595600910287219737299259627413891073174690491219092963035830325, 31474822276849859104123114646070976974921401394140157637420547181522913249875]
    Point4=Curve_demo.minus(Point1,Point2)
    print(Point4)
    #输出：[0, 0]
    Point5=Curve_demo.multiply(Point1,125)
    print(Point5)
    #输出：[110117747631942453047618233423268750303736666185363479400181203180365983524117, 50029238751735848722678415529260555812010873439122287474234503373685614699938]
    print(Curve_demo.check_point(Point1))
    #输出：True
    
 注意：

     其中需保证p为素数，且a、b可构成椭圆曲线，即$$4a^{3}+27b^{2}\neq0$$，否则会报错
    
     Curve对象初始化时还可填其它参数：
        1. G，椭圆曲线上的一个基点，类似于模素数p上的原根
        2. n，基点G的阶

- SM2.py

    SM2公钥加解密模块，其中的群选用椭圆曲线上的点集构成的群

    - 包含一个方法key_generate，基于所给参数随机生成公私钥对及加密所用随机数
    - 包含一个类SM2，用于实现公钥加密、私钥解密
    - 包含一个方法new，基于所给参数返回一个带公私钥对、随机数的SM2实例对象

  具体使用方法如下所示：

    ```python
    #SM2测试

    a = 115792089210356248756420345214020892766250353991924191454421193933289684991996
    b = 18505919022281880113072981827955639221458448578012075254857346196103069175443
    p = 115792089210356248756420345214020892766250353991924191454421193933289684991999
    g = [22963146547237050559479531362550074578802567295341616970375194840604139615431,
         85132369209828568825618990617112496413088388631904505083283536607588877201568]  # 基点
    m = [62220385967324995556943859594383843316990201421105076884209933343560809233015,
         9063699494246492215875763452283052636231938003241827298178711426179690419737]  # 明文点
    n = 62850942488285990642567364045064888609861641279362042129880709558414313  # 基点的阶
    
    from Public_Key_Cipher import SM2
    SM2demo=SM2.new(a,b,p,g,n)
    plaintext=b'123456789'
    cipher=SM2demo.encrypt(plaintext)
    print(cipher)
    #输出：0x04af649749295ee1f0c9f19f29f38947fe2a1207e5cf567ba0e3a6842a64d88856a928bda06f28e37e0aa68ac93bc258865975dd383cd7dea9062ecb43227c10834ae392436a9f6c5f70000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000029227e965c72b06de2610f4c56e8e981635c856b245bdca9c76884a1fa1514fe
    plain=SM2demo.decrypt(str(cipher))
    print(plain)
    #输出：b'123456789'
    print(plain==plaintext)
    #输出：True


### 5. Signature模块

该模块包含了SM2数字签名算法

- SM2_signature.py

    SM2数字签名模块，可实现签名和验证

    - 包含一个参数hash_algorithm，为SM2中所用到的HASH函数,这里调用本密码库中的SM3
    - 包含一个类Sign_And_Verify，用于实现私钥签名、公钥验证
    - 包含一个方法new，基于所给参数返回一个带公私钥对、随机数的Sign_And_Verify实例对象

  具体使用方法如下所示：

    ```python
    #SM2签名
    from Signature import SM2_signature
    #椭圆曲线参数
    prime=60275702009245096385686171515219896416297121499402250955537857683885541941187
    a=54492052985589574080443685629857027481671841726313362585597978545915325572248
    b=45183185393608134601425506985501881231876135519103376096391853873370470098074
    G=[29905514254078361236418469080477708234343499662916671209092838329800180225085,2940593737975541915790390447892157254280677083040126061230851964063234001314]
    n=60275702009245096385686171515219896415919644698453424055561665251330296281527#椭圆曲线的阶
    
    #用户标识
    ID='ALICE123@YAHOO.COM'.encode('utf-8')
    #用户公钥
    PK=[4927346340877997421592888003129352901369751434954921663604743238822873158794,56090775331359075302546016414740579914612192649583459645010750108260086900823]
    #待签名消息
    Message='message digest'.encode('utf-8')
    #私钥
    da=8387551947784012071400071471596312053542870740821494713120726177333060924003
    #随机数
    k=49165263701565432377505549247848435858362931747789390865593867043744446085487
    
    sign=SM2_signature.new(Mode='Sign',a=a,b=b,prime=prime,G=G,n=n,ID=ID,Message=Message,Pk=PK,d=da,k=k)
    print(sign)
    #输出：(29375463689586694004441797766812698475573938256363780089425801847059442521553, 50558071754134037809738440507460307292654583241166284157895327241897986943975)
    verify=SM2_signature.new(Mode='Verify',a=a,b=b,prime=prime,G=G,n=n,ID=ID,Message=Message,Pk=PK,d=da,k=k,r=sign[0],s=sign[1])
    print(verify)
    #输出：True
    



### 6. Hash模块

该模块包含了SM3哈希算法，用于生成消息摘要,支持对文件的摘要

- SM3.py

    SM3哈希模块，可对小于2^64bit长度的消息计算其256位哈希值，可返回hex或bytes

    - 包含一个类SM3，包含update方法、file_hash方法，支持digest、hexdigest方法。

  具体使用方法如下所示：

    ```python
    #SM3测试
    from Hash import SM3
    words='this is the first SM3 testcase.'.encode('utf-8')
    SM3demo=SM3.SM3(words)
    print(SM3demo.hexdigest())
    #输出：0x1c7d1fcf91f37a2ecb8877b5896d3474010784a75cdb1d392375029c4469e653
    print(SM3demo.digest())
    #输出：b'\x1c}\x1f\xcf\x91\xf3z.\xcb\x88w\xb5\x89m4t\x01\x07\x84\xa7\\\xdb\x1d9#u\x02\x9cDi\xe6S'
    Hash=SM3demo.file_hash('D:\download\C2-Solution.pdf')
    print(Hash)
    #输出：0x8781fd10893306c98813b31d0e9be3e035d0c9abb54ac7ec542485eb9fba9e0b

    """
    可用第三方库gmssl进行验证
    """