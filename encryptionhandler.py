from cryptography.fernet import Fernet
import os
import json



def generate_key(key_file='secret.key'):
    """
    Generates a key and saves it to a file.
    """
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)
    print(f"Encryption key generated and saved to {key_file}. Keep this file safe!")
    return key

def load_key(key_file='secret.key'):
    """
    Loads the key from the given file. Generates one if it doesn't exist.
    """
    if not os.path.exists(key_file):
        key = generate_key(key_file)
    else:
        with open(key_file, 'rb') as f:
            key = f.read()
    return key

def encrypt_and_store_entries(entries, key_file='secret.key', output_file='encrypted_entries.bin'):
    """
    Encrypts the entries and stores them to a binary file.
    
    Args:
        entries (list): List of dictionaries containing file entries.
        key_file (str): Path to the encryption key file.
        output_file (str): Path to the output encrypted file.
    """
    key = load_key(key_file)
    fernet = Fernet(key)
    
    # Serialize entries to JSON
    entries_json = json.dumps(entries)
    entries_bytes = entries_json.encode('utf-8')
    
    # Encrypt the data
    encrypted_data = fernet.encrypt(entries_bytes)
    
    # Write the encrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)
    
    print(f"Entries have been encrypted and stored in {output_file}.")