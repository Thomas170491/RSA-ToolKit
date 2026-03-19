# RSA Toolkit: Encryption, Signatures & Attack Simulation

A modular, industry-standard implementation of the RSA (Rivest–Shamir–Adleman) cryptosystem, providing both **Confidentiality** (OAEP) and **Authenticity** (PSS). Powered by a custom-built Miller-Rabin Primality Test engine. Includes a practical **attack simulation** to demonstrate weaknesses in weak RSA implementations.

---

## 🛠 Architecture
This project is designed with **Separation of Concerns**. The core mathematical primitives are maintained in a separate repository and integrated here as a Git Submodule.

* **`main.py`**: The entry point that demonstrates the full encryption and signature lifecycle.
* **`attack_demo.py`**: Demonstrates how RSA can be broken with weak parameters (small primes).
* **`utils/rsa_math.py`**: Handles keypair generation $(e, n)$ and $(d, n)$ using the Extended Euclidean Algorithm.
* **`utils/padding.py`**: Implements **OAEP** padding for secure, non-deterministic encryption.
* **`utils/signatures.py`**: Implements **PSS** encoding for cryptographically secure signatures.
* **Math Engine:** [Prime-Logic-MillerRabin](https://github.com/Thomas170491/Prime-Logic-MillerRabin) - used for cryptographically secure prime generation.

---

## 🚀 Features
- **RSA-OAEP Encryption:** Probabilistic encryption to prevent frequency analysis.
- **RSASSA-PSS Signatures:** Secure digital signing to ensure data integrity and non-repudiation.
- **Tamper Detection:** Built-in demonstration showing how signatures mathematically fail if data is altered.
- **Attack Simulation:** Shows how weak RSA parameters can be exploited to recover private keys.
- **Secure Randomness:** Uses Python's `secrets` module for industry-standard entropy.
- **Miller-Rabin Primality Test:** Implements probabilistic testing to find large 1024-bit primes.

---

## ▶️ Usage

### Run the secure demo:
```bash
python main.py
```
### Run the attack simulation:
```bash
python attack_demo.py
```


## 🧮 Mathematical Background

The security of RSA is based on the **Integer Factorization Problem**. While it is computationally easy to multiply two large prime numbers, it is functionally impossible to factor the result back into the original primes using classical computers.

### 1. Key Generation
1. **Select Primes:** Choose two distinct large primes, $p$ and $q$ (verified via our **Miller-Rabin** engine).  
2. **Compute Modulus ($n$):**  
   $$ n = p \times q $$  
3. **Compute Euler's Totient ($\phi(n)$):**  
   $$ \phi(n) = (p - 1)(q - 1) $$  
4. **Choose Public Exponent ($e$):** We use $65537$ (the 4th Fermat prime).  
5. **Compute Private Exponent ($d$):** Modular multiplicative inverse of $e$ modulo $\phi(n)$:  
   $$ d \cdot e \equiv 1 \pmod{\phi(n)} $$  

### 2. Encryption & Decryption
RSA uses modular exponentiation to transform data.

- **Encryption:**  
  $$ C = M^e \pmod{n} $$  
- **Decryption:**  
  $$ M = C^d \pmod{n} $$  

### 3. Digital Signatures (RSASSA-PSS)
Signatures use the private key to "sign" a message hash.

- **Signing:**  
  $$ S = EM^d \pmod{n} $$  
- **Verification:**  
  $$ EM_{recovered} = S^e \pmod{n} $$  

### 4. Proof of Correctness
The decryption works because of **Euler's Theorem**. Since $d$ is the modular inverse of $e \pmod{\phi(n)}$, we know $ed = 1 + k\phi(n)$ for some integer $k$. Therefore:

$$
C^d \equiv (M^e)^d \equiv M^{ed} \equiv M^{1 + k\phi(n)} \equiv M \cdot (M^{\phi(n)})^k \equiv M \cdot 1^k \equiv M \pmod{n}
$$

---

## 🔴 Attack Simulation

This section demonstrates how **weak RSA parameters (small primes)** can be exploited:

1. Attacker intercepts the public key $(e, n)$.  
2. Factors $n$ into $p$ and $q$.  
3. Recovers the private key $d$.  
4. Decrypts the message without authorization.

> **RSA security depends entirely on the difficulty of factoring large integers.**  
> ⚠️ Small key sizes are trivially breakable.

---

## 🛡️ Security Considerations

### Why OAEP & PSS?
This implementation avoids "Textbook RSA" in favor of **PKCS#1 v2.1**:

- **Semantic Security:** OAEP and PSS introduce a random **seed/salt**, preventing deterministic outputs.  
- **Malleability Protection:** OAEP ensures tampered ciphertexts fail decryption instead of producing predictable changes.  
- **Integrity Check:** PSS ensures any single-bit modification is detected, preventing signature forgery.

---

## 🌍 Real-World Applications

RSA is widely used in:

- TLS / HTTPS (secure web communication)  
- Public Key Infrastructure (PKI)  
- Secure email systems (PGP)  
- Code signing and software verification  

This project demonstrates the same foundational mechanisms used in these systems.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.  

It is **not secure for production** due to:

- Lack of constant-time operations  
- No protection against side-channel attacks  
- Simplified cryptographic implementation  

Use established libraries for real-world applications.

---

## 📦 Installation & Setup

```bash
git clone --recursive https://github.com/Thomas170491/RSA-Key-Gen.git
```


## 📄 License

This project is open-source and distributed under the **MIT License**.  

You are free to **use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies** of this software, provided that the original copyright notice and this permission notice are included in all copies or substantial portions of the software.  

For full details, see the [LICENSE](LICENSE) file.