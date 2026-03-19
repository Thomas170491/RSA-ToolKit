import os
import json
import sys 

sys.path.append(os.path.join(os.getcwd()))

from utils.rsa_math import generate_rsa_keys
from utils.padding import oaep_pad, oaep_unpad
from utils.signatures import pss_encode, pss_verify

KEY_FILE = 'rsa_keys.json'


# -------------------------
# Key Persistence
# -------------------------

def save_keys(private_key : tuple ,public_key : tuple  ) : 
    data : dict[str, dict[str, str]] = {
        "private" : {"d" : str(private_key[0]), "n" : str(private_key[1])},
        "public" :  {"e" : str(public_key[0]), "n" : str(public_key[1])} 
    }
    with open(KEY_FILE, "w") as f :
        json.dump(data,f)

    print(f"[INFO] Keys saved to {KEY_FILE}")

def load_keys() :
    if not os.path.exists(KEY_FILE) :
        return None
    with open(KEY_FILE, "r") as f :
        data = json.load(f) 
    d = int(data["private"]["d"])
    n = int(data["private"]["n"])
    e = int(data["public"]["e"])
    n_pub = int(data["public"]["n"])
    assert n == n_pub, "Public and private modules mismatch"
    return (d,n) , (e,n)

# -------------------------
# Wrapper Functions
# -------------------------

def encrypt_message(message :str, e :int ,n :int) : 
    byte_len = (n.bit_length()+7)//8
    padded = oaep_pad(message.encode(),byte_len)
    cipher_int = pow(int.from_bytes(padded,'big'),e,n)
    cipher_hex =  hex(cipher_int)
    byte_len = (n.bit_length()+7)//8
    padded = oaep_pad(message.encode(),byte_len)
    cipher_int = pow(int.from_bytes(padded,'big'),e,n)
    cipher_hex =  hex(cipher_int)
    print(f"Ciphertext (hex) : {cipher_hex}")
    return cipher_hex

def decrypt_message(cipher_hex : str, d : int, n :int) :
     byte_len = (n.bit_length()+7)//8
     cipher_int = int(cipher_hex,16)
     dec_bytes = pow(cipher_int,d,n).to_bytes(byte_len,'big')
     recovered = oaep_unpad(dec_bytes,byte_len).decode()
     print(f"Decrypted message : {recovered}")
     return recovered
    


def sign_message(message :str, d :int , n :int ) :
     byte_len = (n.bit_length()+7)//8
     em = pss_encode(message.encode(), byte_len)
     sig_int = pow(int.from_bytes(em,'big'), d , n)
     signature = sig_int.to_bytes(byte_len , 'big')
     print(f"Signature (hex): {signature.hex()}")
     return signature  # RETURN BYTES
 

def verify_signature(message: str, signature: bytes, e: int, n: int) -> bool:
    byte_len = (n.bit_length() + 7) // 8
    sig_int = int.from_bytes(signature, 'big')
    recovered_em = pow(sig_int, e, n).to_bytes(byte_len, 'big')
    return pss_verify(message.encode(), recovered_em, byte_len)




    