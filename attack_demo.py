from math import isqrt

def generate_weak_rsa_keys() :
    #Using very small primes (insecure on purpose)
    p = 53
    q=61
    n = p*q
    phi = (p-1)*(q-1)
    e =17

    #Compute d (modular inverse)

    d = pow(e,-1,phi)

    return (d,n), (e,n)

def factor(n) : 
    print(f"[*] Factoring n = {n}")
    for i in range(2,isqrt(n)):
        if n%i == 0:
            return i, n//i
    return None, None

def recover_private_key(p,q, e):
    phi = (p-1)*(q-1)
    return pow(e,-1,phi)

def run_attack():
    print('='*60)
    print("ATTACK DEMO: Breaking Weak RSA")
    print("=" * 60)

    (d,n), (e,n) = generate_weak_rsa_keys()
    print(f"Public Key : e={e}, n={n}")

    p,q = factor(n)

    if p :
        print(f"[!]Found p={p}, q={q}")
        recovered_d = recover_private_key(p,q,e)

        print(f"[!] Recovered private key: d={recovered_d}")

        message = "Hello World!"
        cipher = pow(message,e,n)
        decrypted = pow(cipher, recovered_d, n)


        print(f"[+] Original: {message}")
        print(f"[+] Decrypted with hacked key: {decrypted}")
    else :
        print("Attack failed")


if __name__ == '__main__' :
    run_attack()