import os 
import sys 

sys.path.append(os.path.join(os.getcwd(), 'lib', 'math_engine'))

from src import generate_prime


def extended_gcd(a, b):
    """
    Returns (gcd, x, y) such that ax + by = gcd(a, b)
    Existence is given by Bézout's identity 
    i.e if a,b are two integers, there exists x,y two integers such that
    ax+by = gcd(a,b)
    
    """
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def mod_inverse(e, phi):
    """Calculates the modular multiplicative inverse of e mod phi"""
    d, x, y = extended_gcd(e, phi)
    if d != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

def generate_rsa_keys(bits=1024):
    print(f"[*] Generating a {bits}-bit RSA Keypair...")
    
    # Using Miller-Rabin library for prime generation
    p = generate_prime(bits)
    q = generate_prime(bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Industry standard public exponent
    e = 65537
    
    # Calculating the private exponent
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)
