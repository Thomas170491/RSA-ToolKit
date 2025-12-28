# RSA Toolkit: Encryption & Signatures

A modular, industry-standard implementation of the RSA (Rivest–Shamir–Adleman) cryptosystem, providing both **Confidentiality** (OAEP) and **Authenticity** (PSS). Powered by a custom-built Miller-Rabin Primality Test engine.

## 🛠 Architecture
This project is designed with **Separation of Concerns**. The core mathematical primitives are maintained in a separate repository and integrated here as a Git Submodule.

* **`main.py`**: The entry point that demonstrates the full encryption and signature lifecycle.
* **`utils/rsa_math.py`**: Handles keypair generation $(e, n)$ and $(d, n)$ using the Extended Euclidean Algorithm.
* **`utils/padding.py`**: Implements **OAEP** padding for secure, non-deterministic encryption.
* **`utils/signatures.py`**: Implements **PSS** encoding for cryptographically secure signatures.
* **Math Engine:** [Prime-Logic-MillerRabin](https://github.com/Thomas170491/Prime-Logic-MillerRabin) - used for cryptographically secure prime generation.

## 🚀 Features
- **RSA-OAEP Encryption:** Probabilistic encryption to prevent frequency analysis.
- **RSASSA-PSS Signatures:** Secure digital signing to ensure data integrity and non-repudiation.
- **Tamper Detection:** Built-in demonstration showing how signatures mathematically fail if data is altered.
- **Secure Randomness:** Uses Python's `secrets` module for industry-standard entropy.
- **Miller-Rabin Primality Test:** Implements probabilistic testing to find large 1024-bit primes.

## 🧮 Mathematical Background

The security of RSA is based on the **Integer Factorization Problem**. While it is computationally easy to multiply two large prime numbers, it is functionally impossible to factor the result back into the original primes using classical computers.

### 1. Key Generation
1.  **Select Primes:** Choose two distinct large primes, $p$ and $q$ (verified via our **Miller-Rabin** engine).
2.  **Compute Modulus ($n$):** $$n = p \times q$$
3.  **Compute Euler's Totient ($\phi(n)$):** $$\phi(n) = (p - 1)(q - 1)$$
4.  **Choose Public Exponent ($e$):** We use $65537$ (the 4th Fermat prime).
5.  **Compute Private Exponent ($d$):** This is the modular multiplicative inverse of $e$ modulo $\phi(n)$.
    $$d \cdot e \equiv 1 \pmod{\phi(n)}$$

### 2. Encryption & Decryption
RSA uses modular exponentiation to transform data. 

* **Encryption:** To encrypt a message $M$, we calculate the ciphertext $C$:
    $$C = M^e \pmod{n}$$
* **Decryption:** To recover the message, we use the private key $d$:
    $$M = C^d \pmod{n}$$

### 3. Digital Signatures (RSASSA-PSS)
Signatures use the private key to "sign" a message hash, allowing anyone with the public key to verify its origin.



* **Signing:** The message is hashed and padded with random salt (PSS) to create an encoded block $EM$.
    $$S = EM^d \pmod{n}$$
* **Verification:** The receiver recovers the encoded block using the public key.
    $$EM_{recovered} = S^e \pmod{n}$$

### 4. Proof of Correctness
The decryption works because of **Euler's Theorem**. Since $d$ is the modular inverse of $e \pmod{\phi(n)}$, we know that $ed = 1 + k\phi(n)$ for some integer $k$. Therefore:

$$C^d \equiv (M^e)^d \equiv M^{ed} \equiv M^{1 + k\phi(n)} \equiv M \cdot (M^{\phi(n)})^k \equiv M \cdot 1^k \equiv M \pmod{n}$$

## 🛡️ Security Considerations

### Why OAEP & PSS?
This implementation avoids "Textbook RSA" in favor of the **PKCS#1 v2.1** standard:

1. **Semantic Security:** OAEP and PSS introduce a random **seed** or **salt**. The same input never produces the same output twice, preventing frequency analysis.
2. **Malleability Protection:** OAEP's **Feistel Network** structure ensures that any tampering with the ciphertext results in an invalid decryption rather than a predictable change in the message.
3. **Integrity Check:** PSS includes a hash-based verification. If an attacker modifies even a single bit of the signed document, the signature verification will fail.



## 📦 Installation & Setup
To clone this project along with its dependencies:
```bash
git clone --recursive [https://github.com/Thomas170491/RSA-Key-Gen.git](https://github.com/Thomas170491/RSA-Key-Gen.git)
```

This project is open-source and available under the MIT License. See LICENSE file for more info.