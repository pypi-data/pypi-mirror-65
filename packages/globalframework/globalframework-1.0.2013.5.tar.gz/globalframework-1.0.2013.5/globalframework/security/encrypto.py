# default libraries

import hashlib

# Third party libraries
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Globalframework packages
from globalframework.data.setting import Setting


class Crypto():

    def __init__(self):
        self.fernetkey = ""

    def generate_symmetric_key(self):
        """Generate Fernet symmetric key"""
        self.fernetkey = Fernet.generate_key()
        return self.fernetkey

    def encrypt(self, plaintext: str, key: str):
        """Encrypt plaintext using Fernet to cipher using symmetric encryption"""
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(plaintext.encode())
        return cipher_text

    def decrypt(self, ciphertext: str, key: str):
        """Decrypt cipher using Fernet to plaintext using symmetric encryption"""
        return self.decrypt_with_sliding_window(ciphertext, key, None)

    def decrypt_with_sliding_window(self, ciphertext: str, key: str, second: int):
        """Decrypt cipher using Fernet to plaintext with a sliding window in seconds how old a message may be for it to be valid
        using symmetric encryption"""
        cipher_suite = Fernet(key)
        plaintext = cipher_suite.decrypt(ciphertext, second)
        return plaintext.decode()

    def encrypt_file(self, key: str, filename: str, newfilename=""):
        """ Load a given file, encrypt content and write to a specified file name
            If new file name is not given rename file with an addition of 'en_'
        """
        encrypted_file_name = newfilename
        setting = Setting()
        if not newfilename:
            # if the encrypted filename is not provided use the source filename and add an en_.
            encrypted_file_name = setting.rename_file(filename, '\\en_')

        content = setting.load_file_content_byte(filename)
        cipher_suite = Fernet(key)

        encrypted_content = cipher_suite.encrypt(content)

        setting.write_file_byte(encrypted_file_name, encrypted_content)
        return encrypted_file_name

    def decrypt_file(self, key: str, filename: str, newfilename=""):
        """ Load a given file, decrypt content and write to a specified file name
            If new file name is not given rename file with an addition of 'de_'
        """
        decrypted_file_name = newfilename
        setting = Setting()
        if not newfilename:
            # if the encrypted filename is not provided use the source filename and add an dn_.
            decrypted_file_name = setting.rename_file(filename, '\\de_')

        content = setting.load_file_content_byte(filename)
        cipher_suite = Fernet(key)

        decrypted_content = cipher_suite.decrypt(content)

        setting.write_file_byte(decrypted_file_name, decrypted_content)
        return decrypted_file_name

    def hash_with_sha2(self, inputtext: str):
        """ Hash string using SHA2 hashing algorithm """
        output = self.hashing_input(inputtext, hashes.SHA256())
        return output

    def hash_with_blake2s(self, inputtext: str):
        """ Hash string using BLAKE2 hashing algorithm """
        output = self.hashing_input(inputtext, hashes.BLAKE2s(32))
        return output

    def hashing_input(self, inputtext: str, hashtype):
        """ Hash input based on primitive type"""
        input_to_hash = bytes(inputtext, 'utf-8')
        digest = hashes.Hash(hashtype, backend=default_backend())
        digest.update(input_to_hash)
        output = digest.finalize()

        return output

    def lookupHashMethod(self, algorithm: str):
        return getattr(self, 'hash_with_' + algorithm, None)

    def hash_content(self, password: str, algorithm: str):
        method = self.lookupHashMethod(algorithm)
        result = method(password)
        return result

    def hashlib_sha2(self, inputtext: str):
        """ Hash with SHA2 """
        input_to_hash = bytes(inputtext, 'utf-8')
        output = hashlib.sha256(input_to_hash)
        return output

    def hashlib_blake2s(self, inputtext: str):
        """ Hash with Blake2s """
        input_to_hash = bytes(inputtext, 'utf-8')
        output = hashlib.blake2s(input_to_hash)
        return output
