#-----------------------------------------------------------------------

#Semih Balki - 19010
#Elif Rahmiye Kulunk - 20830
#Python IDE: PyCharm
#Operating system: MacOS

#-----------------------------------------------------------------------
import random
import math
import string
import hashlib
import os.path
import DS_Test

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

# taken from the homework 4 document
def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


#Following 3 functions taken from: https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
def isPrime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = random.getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in          bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not isPrime(p, 128):
        p = generate_prime_candidate(length)
    return p


def nextprime(x):
    xx = x;

    while isPrime(xx) == False:
        xx += 1

    return xx


def GenerateOrRead(filename):
    if os.path.isfile(filename):#If file exists read it
        f = open(filename, "r")
        q = f.readline()
        p = f.readline()
        g = f.readline()
        f.close()
        if PubParamcheck(int(q), int(p), int(g)) == 0:
            return int(q), int(p), int(g)
    else:#else, generate new parameters
        q, p, g = PubParam(2**224, 2**2048, None)
        f = open(filename,"w")
        f.write(str(q)+"\n")
        f.write(str(p)+"\n")
        f.write(str(g))
        f.close()
    return q, p, g

def PubParam(q_length, p_length, g_length):
    #generate g, p and a.(q->224 bits)(p->2048 bits)
    q_length = int(math.log(q_length, 2))#extract the length of the q and p by log in base 2
    p_length = int(math.log(p_length, 2))
    q = generate_prime_number(q_length)

    while True:#To form p which is 2048 bit and (p - 1) % q = 0
        n = random.getrandbits(p_length - q_length)
        p = (q * n) + 1
        if isPrime(p):
            break

    while True:# n = (p - 1) / q
        alpha = random.randint(1, (p - 1))
        g = pow(alpha, n, p)
        if g != 1 and type(g) == int:
            break

    return q, p, g


def PubParamcheck(q, p, g):#Check parameters at DSA_Test
    if DS_Test.checkDSparams(q, p, g) == 0:
        return 0

    return -1


def KeyGen(q, p, g):
    alpha = random.randint(1, q - 1)
    B = pow(g, alpha, p)

    return alpha, B


def random_string(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def SignGen(m, q, p, g, alpha):
    k = random.randint(0, q - 1)
    r = pow(g, k, p)
    r = str(r).encode('UTF-8')
    h = hashlib.sha3_256()
    h.update(m)
    h.update(r)#m + r
    s = ((alpha * int(h.hexdigest(), 16)) + k)
    s %= q
    h = int(h.hexdigest(), 16)
    return s, h


def SignVer(m, s, h, q, p, g, B):
    B_inv = modinv(B, p)
    hold = s % (p - 1)#when we work in mod p in the base, we can work phi(p) in the exponent
    hold_1 = h % (p - 1)
    e = pow(g, hold, p)
    j = pow(B_inv, hold_1, p)
    v = (e * j) % p
    v = str(v).encode('UTF-8')
    h_bar = hashlib.sha3_256()
    h_bar.update(m)
    h_bar.update(v)#by updating, concatenate m and v
    h_bar = int(h_bar.hexdigest(), 16)
    if (h % q) == (h_bar % q):
        return 0

    return -1