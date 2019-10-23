#-----------------------------------------------------------------------

#Semih Balki - 19010
#Elif Rahmiye Kulunk - 20830
#Python IDE: PyCharm
#Operating system: MacOS

#-----------------------------------------------------------------------

import random
import hashlib


def PoW(PoWLen, q, p, g, filename):
    f = open(filename, "r")
    block = f.readlines()
    block = "".join(block)
    block += "Nonce: "

    while True:
        nonce = str(random.getrandbits(128)) + "\n"
        possible = block + nonce
        hashed = hashlib.sha3_256(possible.encode('UTF-8')).hexdigest()

        if hashed[0:PoWLen] == "0" * PoWLen:
            break

    return possible