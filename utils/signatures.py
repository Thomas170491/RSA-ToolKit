import hashlib
import os
from utils.padding import mgf1

def pss_encode(message_bytes, k, salt_len=32):
    """
    Encodes a message for signing using the PSS scheme.
    k: length of the RSA modulus in bytes (128 for 1024-bit).
    """
    h_len = hashlib.sha256().digest_size
    # 1. Hash the original message
    m_hash = hashlib.sha256(message_bytes).digest()
    
    # 2. Check if the block is big enough
    if k < h_len + salt_len + 2:
        raise ValueError("Key size too small for PSS parameters")

    # 3. Generate random salt
    salt = os.urandom(salt_len)
    
    # 4. Create M' = (0x00 * 8) + m_hash + salt
    m_prime = b"\x00" * 8 + m_hash + salt
    h = hashlib.sha256(m_prime).digest()
    
    # 5. Create Data Block (DB) = PS + 0x01 + salt
    ps = b"\x00" * (k - h_len - salt_len - 2)
    db = ps + b"\x01" + salt
    
    # 6. Mask the DB
    db_mask = mgf1(h, k - h_len - 1)
    masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
    
    # 7. Final encoded message (EM)
    # The last byte 0xbc is the PSS trailer field
    return masked_db + h + b"\xbc"

def pss_verify(message_bytes, encoded_msg, k, salt_len=32):
    """
    Verifies the PSS encoded message against the original message.
    """
    h_len = hashlib.sha256().digest_size
    
    # 1. Basic checks
    if encoded_msg[-1:] != b"\xbc":
        return False
    
    # 2. Split the encoded message
    masked_db = encoded_msg[:k - h_len - 1]
    h = encoded_msg[k - h_len - 1 : -1]
    
    # 3. Recover DB
    db_mask = mgf1(h, k - h_len - 1)
    db = bytes(a ^ b for a, b in zip(masked_db, db_mask))
    
    # 4. Extract Salt
    # The first (k - h_len - salt_len - 2) bytes should be 0x00
    # Then a 0x01 separator, then the salt.
    ps_len = k - h_len - salt_len - 2
    salt = db[-salt_len:]
    
    # 5. Reconstruct M' and check Hash
    m_hash = hashlib.sha256(message_bytes).digest()
    m_prime = b"\x00" * 8 + m_hash + salt
    h_check = hashlib.sha256(m_prime).digest()
    
    return h == h_check