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

def decrypt_and_load_entries(encrypted_file='encrypted_entries.bin', key_file='secret.key'):
    """
    Decrypts the encrypted entries stored in the binary file and loads them as a list of dictionaries.
    
    Args:
        encrypted_file (str): Path to the encrypted binary file.
        key_file (str): Path to the encryption key file.
    
    Returns:
        list: A list of dictionaries containing the decrypted file entries.
    """
    # Load the encryption key
    key = load_key(key_file)
    fernet = Fernet(key)
    
    # Read the encrypted data from the file
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()
    
    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data)
    
    # Deserialize the data from JSON format
    entries_json = decrypted_data.decode('utf-8')
    entries = json.loads(entries_json)
    
    print(f"Decrypted entries: {entries}")
    return entries
