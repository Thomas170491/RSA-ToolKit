import hashlib
import secrets

def mgf1(seed, length, hash_func=hashlib.sha256):
    # 1. Initialize an empty byte string to hold our mask
    mask = b""
    
    # 2. Initialize a counter starting at 0
    # This ensures that every hash we generate is unique
    counter = 0
    
    # 3. Start a loop that runs until we have enough bytes
    # length is the target size (e.g., 95 bytes for the Data Block)
    while len(mask) < length:
        
        # 4. Convert the counter into a 4-byte block (Big Endian)
        # e.g., 0 becomes b'\x00\x00\x00\x00', 1 becomes b'\x00\x00\x00\x01'
        C = counter.to_bytes(4, byteorder='big')
        
        # 5. Hash the seed combined with the counter
        # This creates a unique 32-byte "chunk" of random-looking data
        mask += hash_func(seed + C).digest()
        
        # 6. Increment the counter for the next round
        counter += 1
    
    # 7. Truncate the mask to the exact length requested
    # Since SHA-256 gives 32 bytes at a time, we might have too much (e.g., 96 instead of 95)
    return mask[:length]

def oaep_pad(message_bytes, k, label=b""):
    # 1. Get the hash size (SHA-256 = 32 bytes)
    h_len = hashlib.sha256().digest_size

    # 2. Safety check: Is the message too big to fit in the 128-byte block?
    # We need room for 2 hashes, a separator, and a leading zero.
    if len(message_bytes) > k - 2 * h_len - 2:
        raise ValueError("Message too long")
    
    # 3. Create a random seed (32 bytes of entropy)
    # This ensures probabilistic encryption (different result every time)
    seed = secrets.token_bytes(h_len)
    
    # 4. Create the Data Block (DB)
    # [L_HASH] + [PADDING_ZEROS] + [0x01_SEPARATOR] + [MESSAGE]
    l_hash = hashlib.sha256(label).digest()
    padding = b"\x00" * (k - len(message_bytes) - 2 * h_len - 2)
    db = l_hash + padding + b"\x01" + message_bytes
    
    # 5. Mask the Data Block
    # We use MGF1 to stretch the seed into a mask the size of our DB
    db_mask = mgf1(seed, k - h_len - 1)
    # XOR the DB with the mask (Scramble the message)
    masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
    
    # 6. Mask the Seed
    # Use the scrambled DB to create a mask for the seed
    seed_mask = mgf1(masked_db, h_len)
    # XOR the seed with the mask (Scramble the seed)
    masked_seed = bytes(a ^ b for a, b in zip(seed, seed_mask))
    
    # 7. Return the final 128-byte block (Starting with a 0x00 byte)
    return b"\x00" + masked_seed + masked_db

def oaep_unpad(padded_bytes, k, label=b""):
    h_len = hashlib.sha256().digest_size
    
    # 1. Split the 128-byte block back into its components
    # (Ignoring the first 0x00 byte)
    masked_seed = padded_bytes[1:1+h_len]
    masked_db = padded_bytes[1+h_len:]
    
    # 2. Recover the Seed
    # Create the seed_mask from the masked_db and XOR it back
    seed_mask = mgf1(masked_db, h_len)
    seed = bytes(a ^ b for a, b in zip(masked_seed, seed_mask))
    
    # 3. Recover the Data Block (DB)
    # Create the db_mask from the recovered seed and XOR it back
    db_mask = mgf1(seed, k - h_len - 1)
    db = bytes(a ^ b for a, b in zip(masked_db, db_mask))
    
    # 4. Integrity Check
    # Compare the hash inside the DB to a fresh hash of the label
    if db[:h_len] != hashlib.sha256(label).digest():
        raise ValueError("OAEP integrity check failed")
        
    # 5. Find the Message
    # Look for the 0x01 byte. Everything after it is your text.
    separator_index = db.find(b"\x01", h_len)
    return db[separator_index + 1:]