# 🧮 Mathematical Background

The security of RSA is based on the **Integer Factorization Problem**. While it is computationally easy to multiply two large prime numbers, it is functionally impossible to factor the result back into the original primes using classical computers.

## 1. Key Generation

- **Select Primes:** Choose two distinct large primes, \(p\) and \(q\) (verified via our Miller-Rabin engine).  

- **Compute Modulus (\(n\)):**  

$$
n = p \times q
$$

- **Compute Euler's Totient (\(\phi(n)\)):** 

$$
\phi(n) = (p - 1)(q - 1)
$$

- **Choose Public Exponent (\(e\)):** We use 65537 (the 4th Fermat prime).  
- **Compute Private Exponent (\(d\)):** Modular multiplicative inverse of \(e\) modulo \(\phi(n)\):

$$
d \cdot e \equiv 1 \pmod{\phi(n)}
$$

---

## 2. Encryption & Decryption

RSA uses modular exponentiation to transform data.

- **Encryption:**  

$$
C = M^e \pmod{n}
$$

- **Decryption:**  

$$
M = C^d \pmod{n}
$$

---

## 3. Digital Signatures (RSASSA-PSS)

Signatures use the private key to "sign" a message hash.

- **Signing:**  

$$
S = EM^d \pmod{n}
$$

- **Verification:** 
 
$$
EM_{recovered} = S^e \pmod{n}
$$  

## 4. Proof of Correctness
The decryption works because of **Euler's Theorem**. Since $d$ is the modular inverse of $e \pmod{\phi(n)}$, we know $ed = 1 + k\phi(n)$ for some integer $k$. Therefore:

$$
C^d \equiv (M^e)^d \equiv M^{ed} \equiv M^{1 + k\phi(n)} \equiv M \cdot (M^{\phi(n)})^k \equiv M \cdot 1^k \equiv M \pmod{n}
$$