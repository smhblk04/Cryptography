#-----------------------------------------------------------------------

#Semih Balki - 19010
#Elif Rahmiye Kulunk - 20830
#Python IDE: PyCharm
#Operating system: MacOS

#-----------------------------------------------------------------------


import string
import sys
import random
import hashlib


def gen_random_tx(q, p, g):
    string = "*** Bitcoin transaction ***\n"

    serial = random.getrandbits(128)
    string += "Serial number: " + str(serial) + "\n"

    payer_alpha = random.randint(1, q - 1)
    payer_beta = pow(g, payer_alpha, p)

    string += "Payer Public Key (beta): " + str(payer_beta) + "\n"

    payee_alpha = random.randint(1, q - 1)
    payee_beta = pow(g, payee_alpha, p)

    string += "Payee Public Key (beta): " + str(payee_beta) + "\n"

    amount = random.randint(1, 1000000)
    string += "Amount: " + str(amount) + " Satoshi" + "\n"

    # compute signature

    k = random.randint(1, q - 1)
    r = pow(g, k, p)
    r = str(r).encode('UTF-8')
    h = hashlib.sha3_256()
    h.update(string.encode('UTF-8'))
    h.update(r)  # m + r
    s = ((payer_alpha * int(h.hexdigest(), 16)) + k)
    s %= q
    h = int(h.hexdigest(), 16)

    string += "Signature (s): " + str(s) + "\n"
    string += "Signature (h): " + str(h) + "\n"

    return string