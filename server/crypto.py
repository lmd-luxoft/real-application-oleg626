# Copyright 2019 by Kirill Kanin.
# All rights reserved.

import os
import hashlib
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes
from typing import Tuple, BinaryIO
from server.singleton import SingletonType

key_folder = os.environ['KEY_DIR']


class HashAPI:
    """Class with static methods for generating hashes.

    """

    @staticmethod
    def hash_sha512(input_str: str) -> str:
        """Generate hash SHA-512.

        Args:
            input_str (str): Input string.

        Returns:
            Str with hash in hex format.

        Raises:
            AssertionError: if input string is not set.

        """

        pass

    @staticmethod
    def hash_md5(input_str: str) -> str:
        """Generate hash MD5.

        Args:
            input_str (str): Input string.

        Returns:
            Str with hash in hex format.

        Raises:
            AssertionError: if input string is not set.

        """
        try:
            assert len(input_str) > 0, "Input string is empty"

            hash_obj = hashlib.md5(input_str.encode())
            return hash_obj.hexdigest()
        except AssertionError as msg:
            print(msg)


class BaseCipher(metaclass=SingletonType):
    """Base cipher class.

    """

    def __init__(self):
        pass

    def encrypt(self, data: bytes):
        """Encrypt data.

        Args:
            data (bytes): Input data for encrypting.

        """

        pass

    def decrypt(self, input_file: BinaryIO) -> bytes:
        """Decrypt data.

        Args:
            input_file (BinaryIO): Input file with data for decrypting.

        Returns:
            Bytes with decrypted data.

        """

        pass

    def write_cipher_text(self, data: bytes, out_file: BinaryIO):
        """Encrypt data and write cipher text into output file.

        Args:
            data (bytes): Encrypted data,
            out_file(BinaryIO): Output file.

        """

        pass


class AESCipher(BaseCipher):
    """AES cipher class.

    """

    def __init__(self):
        self.__key__ = get_random_bytes(16)
        pass

    def encrypt(self, data: bytes, key: bytes = None) -> Tuple[bytes, bytes, bytes, bytes]:
        """Encrypt data.

        Args:
            data (bytes): Input data for encrypting.
            key (bytes): AES key

        Returns:
            Tuple with bytes values, which contains cipher text, tag, nonce and session key.

        """
        if key is None:
            key = self.__key__
        cipher = AES.new(key, AES.MODE_EAX)
        cipher_text, tag = cipher.encrypt_and_digest(data)
        return cipher_text, tag, cipher.nonce

    def decrypt(self, filename: BinaryIO, key_file: str) -> bytes:
        """Decrypt data.

        Args:
            filename (BinaryIO): Input file with data for decrypting.

        Returns:
            Bytes with decrypted data.

        """
        with open(filename, 'rb') as f:
            nonce, tag, cipher_text = [f.read(x) for x in (16, 16, -1)]

        with open(key_file, 'rb') as f:
            key_bytes = f.read()
        cipher = AES.new(key_bytes, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(cipher_text, tag)
        return data

    def generate_AES_key(self):
        """ generate AES key and save it to file

        filename (str): Name of the file to save AES key

        """
        key_bytes = get_random_bytes(16)

        self.__key__ = key_bytes
        return key_bytes

    def get_key(self):
        return self.__key__


class RSACipher(AESCipher):
    """RSA cipher class.

    """

    def __init__(self, user_id: int):
        pass

    def encrypt(self, data: bytes) -> Tuple[bytes, bytes, bytes, bytes]:
        """Encrypt data.

        Args:
            data (bytes): Input data for encrypting.

        Returns:
            Tuple with bytes values, which contains cipher text, tag, nonce and session key.

        """

        pass

    def decrypt(self, input_file: BinaryIO) -> bytes:
        """Decrypt data.

        Args:
            input_file (BinaryIO): Input file with data for decrypting.

        Returns:
            Bytes with decrypted data.

        """

        pass

    def write_cipher_text(self, data: bytes, out_file: BinaryIO):
        """Encrypt data and write cipher text into output file.

        Args:
            data (bytes): Encrypted data,
            out_file(BinaryIO): Output file.

        """

        pass
