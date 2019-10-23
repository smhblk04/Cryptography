#-----------------------------------------------------------------------

#Semih Balki - 19010
#Elif Rahmiye Kulunk - 20830
#Python IDE: PyCharm
#Operating system: MacOS

#-----------------------------------------------------------------------
import random
import hashlib
from ecpy.curves import Curve, Point
from ecpy.keys import ECPublicKey, ECPrivateKey
from ecpy.ecdsa import ECDSA
from ecpy.formatters import decode_sig, encode_sig


def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


#curve = Curve.get_curve('secp256k1')
def gen_random_tx(curve):
    n = curve.order
    P = curve.generator
    sA = random.randint(0, n)
    sk = ECPrivateKey(sA, curve)
    QA = sA * P
    pk = ECPublicKey(QA)

    payee_sA = random.randint(0, n)
    payee_sk = ECPrivateKey(payee_sA, curve)
    payee_QA = sA * P
    payee_pk = ECPublicKey(payee_QA)

    sum_string = "*** Bitcoin transaction ***\n"

    serial = random.getrandbits(128)
    sum_string += "Serial number: " + str(serial) + "\n"

    sum_string += "Payer Public key - x: " + str(QA.x) + "\n"

    sum_string += "Payer Public key - y: " + str(QA.y) + "\n"

    sum_string += "Payee Public key - x: " + str(payee_QA.x) + "\n"

    sum_string += "Payee Public key - y: " + str(payee_QA.y) + "\n"

    amount = random.randint(1, 1000000)
    sum_string += "Amount: " + str(amount) + " Satoshi" + "\n"

    signer = ECDSA()

    sig = signer.sign(sum_string.encode('UTF-8'), sk)

    (r, s) = decode_sig(sig)

    # k = random.randint(1, n - 1)
    # R = k * P
    # r = R.x % n
    # #r = str(r).encode('UTF-8')
    # h = hashlib.sha3_256()
    # h.update(sum_string.encode('UTF-8'))
    # # h.update(str(r).encode('UTF-8'))
    # #h.update(r)  # m + r
    # s = (modinv(k, n) * ((int(h.hexdigest(), 16)) + (sA * r))) % n
    # #h = int(h.hexdigest(), 16)

    sum_string += "Signature - r: " + str(r) + "\n"

    sum_string += "Signature - s: " + str(s) + "\n"

    return sum_string