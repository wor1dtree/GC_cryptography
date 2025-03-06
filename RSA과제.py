import random

def abmodn(a, b, n):
    binary = []

    k = 1 # 반복횟수
    while (b >= 2 ** k):
        k += 1

    for i in range(k-1,-1, -1): #바이너리 만들기    
        if (b >= 2**i):
            b -= 2**i
            binary.append(1)
        else :
            binary.append(0)

#9장에 나온 지수 계산
    f = 1 
    for i in range(0, k):
        f = (f * f) % n # a^k mod n * a^k mod n = a^2k mod n
        if(binary[i] == 1):
            f = (f * a) % n #a^p mod n * a^q = a^(p+q) mod n
    return f

def millerRabinTest(testPrime, time) :
    if (testPrime%2 == 0): #짝수는 모두 소수가 아님
        return 0 # 0은 합성수 1은 소수

    temp = testPrime - 1    # temp = (2^k)*q 으로 표현하고자 함 q은 홀수
    k = 0
    while(1):    
        if(temp % 2 == 0):
            temp = temp/2
            k += 1
        else :
            break
    
    count = 0
    check = 1 # 통과하면 소수이므로 1
    while (count < time): #time번 시도
        a = random.randint(2, testPrime-1)
        
        if (abmodn(a, temp, testPrime) == 1) : #inconclusive됨
            check = 1
        else : 
            for j in range(0,k): 
                if(abmodn(a, 2*j*temp, testPrime) == testPrime - 1) : #(testPrime - 1) mod testPrime = -1이다
                    check = 1
                else :
                    return 0 # 합성수
        count += 1        
    return 1 #소수



def makePrime(min, max, time):  #소수 만드는 함수, min은 최솟값, max는 최댓값, time은 검사 횟수
    testPrime = 0
    while(1):
        testPrime = random.randint(min,max) #소수 후보를 생성함
        if (millerRabinTest(testPrime, time) == 1):  #밀러라빈테스트를 통해 소수 여부 확인
            break
    return testPrime #소수 반환

def checkgcd1(a, b): # a = bq + r
    while(1) : 
        if (a % b == 0):
            break
        temp = a
        a = b
        b = temp % b
        
    return b

def findd(e, n): #확장 유클리드 알고리즘을 활용하여 d값을 찾았다 ,  e => n 
    r = [n, e]
    q = [0, 0]
    y = [0, 1]

    i = 0
    while(r[i+1] != 0):
        q.append(r[i] // r[i+1])
        y.append(y[i] - q[i+2] * y[i+1])
        r.append(r[i] - q[i+2] * r[i+1])
        i += 1

    if (y[i] <= 0) : #음수의 경우 양수로 바꾸어 주었다.
        y[i] += n

    return (y[i])
    

def makeKey(p,q):
    n = p*q     
    e = 65537   #pi(n)의 최솟값이 90000이므로 e = 65537을 선택해도 된다

    if(checkgcd1(p-1, e) != 1 or checkgcd1(q-1, e) != 1):
        print("gcd(p-1,e)또는 gcd(q-1,e)가 1이 아닙니다")
        exit(-1)
    
    d = findd(e, (p-1)*(q-1))
    
    return (e, n, d, p, q)

def decrypt(m, e, n):
    ciphertext = []
    for i in range(len(m)): #나누어서 암호화
        ciphertext.append(abmodn(ord(m[i]), e, n))

    return ciphertext

def encrypt(c, d, n):
    plaintext = []

    for i in range(len(c)):
        plaintext.append(abmodn(c[i], d, n))

    return plaintext

def encryptWithCrt(c, d ,p, q): #중국인의 나머지 정리를 이용한 복호화
    plaintext = []

    for i in range(len (c)):    
        dp = d % (p-1)
        dq = d % (q-1)
        if (p > q):
            inv = findd(q, p)
        else :
            inv = findd(p, q)

        m1 = abmodn(c[i],dp,p)
        m2 = abmodn(c[i],dq,q)

        h = (inv * (m1 - m2)) % p
        m = m2 + h * q
        plaintext.append(m)

    return plaintext


#---------------------시작 부분-------------------
min = 300
max = 10000
time = 10
while(1):
    p = makePrime(min, max, time)
    q = makePrime(min, max, time)
    if(p != q):
        break

(e, n, d, p, q) = makeKey(p,q)
print(e, n, d, p, q) #key 출력

message = "Give me a+, please!"

ciphertext = decrypt(message, e, n) # 암호화
print("암호문 : ")
print(ciphertext)

plaintext = encryptWithCrt(ciphertext, d, p, q) # 복호화

message2 = "".join(chr(code) for code in plaintext)

print("평문 : " + message)
print("복호화된 평문 : " + message2)
