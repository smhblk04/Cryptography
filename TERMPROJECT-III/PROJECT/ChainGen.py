#-----------------------------------------------------------------------

#Semih Balki - 19010
#Elif Rahmiye Kulunk - 20830
#Python IDE: PyCharm
#Operating system: MacOS

#-----------------------------------------------------------------------
import hashlib
import random

def AddBlock2Chain(PoWLen, PrevBlock, NewBlock):
    if PrevBlock == 0:
         NewBlock += "Previous Hash: b '0'" + "\n"
    if PrevBlock != 0 and type(PrevBlock) != int:
        hashed = hashlib.sha3_256(PrevBlock.encode('UTF-8')).hexdigest()
        NewBlock += "Previous Hash: " + str(hashed) + "\n"

    NewBlock += "Nonce: "
    possible = ""
    while True:
        nonce = str(random.getrandbits(128)) + "\n"
        possible = NewBlock + nonce
        hashed = hashlib.sha3_256(possible.encode('UTF-8')).hexdigest()

        if hashed[0:PoWLen] == "0" * PoWLen:
            break

    return possible