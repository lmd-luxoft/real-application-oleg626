# Copyright 2019 by Kirill Kanin.
# All rights reserved.

import argparse
import os
import sys
import logging
import json
from server.crypto import AESCipher
from aiohttp import web
from server.handler import Handler
#from server.database import DataBase
from server.file_service import FileService, FileServiceSigned


def commandline_parser() -> argparse.ArgumentParser:
    """Command line parser.

    Parse port and working directory parameters from command line.

    -p --port - port (default: 8080).
    -f --folder - working directory (absolute or relative path, default: current app folder FileServer).
    -i --init - initialize database.
    -h --help - help.

    """
    p = argparse.ArgumentParser(
        description='Please specify following arguments')
    p.add_argument('-p', '--port', metavar='PORT', type=int, default=8080,
                   help='port for application')
    p.add_argument('-d', '--directory', metavar='DIR', type=str, default="C:/",
                   help='working directory')
    p.add_argument('-i', '--init', action='store_true', default=False,
                   help='initialize database')

    return p


def get_files():
    files = FileServiceSigned().get_files()
    return files

def get_file_data(filename):
    """Get full info about file.

    Args:
        filename (str): Working directory path.

    Returns:
        Dict, which contains full info about file. Keys:
            name (str): name of file with .txt extension.
            content (str): file content.
            create_date (str): date of file creation.
            edit_date (str): date of last file modification.
            size (int): size of file in bytes.

    Raises:
        AssertionError: if file does not exist, filename format is invalid,
        ValueError: if security level is invalid.

    """
    file_data = FileServiceSigned().get_file_data(filename)
    return file_data


def create_file(file_name):
    """Create new .txt file.

    Method generates name of file from random string with digits and latin letters.

    Args:
        file_name (str): file to create without .txt extension.

    Returns:
        Dict, which contains name of created file. Keys:
            name (str): name of file with .txt extension.
            content (str): file content.
            create_date (str): date of file creation.
            size (int): size of file in bytes,
            user_id (int): user Id.

    Raises:
        AssertionError: if user_id is not set,
        ValueError: if security level is invalid.

    """
    file_content = input("Enter file content: ")

    return FileServiceSigned().create_file(file_name, file_content)


def delete_file(filename):
    """Delete file.

    Args:
        filename (str): File to delete without .txt extension

    Returns:
        Str with filename with .txt file extension.

    Raises:
        AssertionError: if file does not exist.

    """
    return FileServiceSigned().delete_file(filename)


def change_dir(path):
    """Change working directory.

    Args:
        path (str): Working directory path.

    Returns:
        Str with successfully result.

    """
    FileServiceSigned().change_dir(path)


def generate_AES_key(filename):
    """ generates AES key and saves it to file

    Args:
        filename (str): Name of the file

    """
    key_bytes = AESCipher().generate_AES_key()
    FileServiceSigned().create_file(filename, key_bytes.decode())

def encrypt_file_AES(filename: str, key_file: str):
    """ encrypt a file

    :param filename (str): File to encrypt
    :paran key_file (str): File with encryption key
    """
    with open(key_file, 'r') as f:
        key = f.read()
        key_bytes = key.encode()

    with open(filename, 'r') as f:
        data = f.read()
        cipher_text, tag, nonce = AESCipher().encrypt(data.encode(), key_bytes)

    with open(filename[:-4] + '_e.bin', 'wb') as f:
        [f.write(x) for x in (nonce, tag, cipher_text)]

    return cipher_text


def decrypt_file_AES(filename: str, key_file: str, save_to: str):
    data = AESCipher().decrypt(filename, key_file)

    FileServiceSigned().create_file(save_to, data.decode())


def main():
    """Entry point of app
    Get and parse command line parameters and configure web app.
    Command line options:
    -p --port - port (default: 8080).
    -f --folder - working directory (absolute or relative path, default: current app folder FileServer).
    -i --init - initialize database.
    -h --help - help.
    """

    args = commandline_parser().parse_args()

    while True:
        command = str(input("Enter the command: "))
        if command.startswith("create "):
            create_file(command[7:])
        elif command.startswith("get "):
            print(get_file_data(command[4:]))
        elif command.startswith("list"):
            for file in get_files():
                print(file)
        elif command.startswith("delete "):
            delete_file(command[7:])
        elif command.startswith("encrypt "):
            filename = command[8:]
            aes_key_file = input("Enter key file name: ")
            print(f'generated key %s' % generate_AES_key(aes_key_file))
            encrypt_file_AES(filename, aes_key_file)
        elif command.startswith("decrypt "):
            filename = command[8:]
            key_file = input("Enter keyfile to use: ")
            save_to = input("Enter file to save: ")
            decrypt_file_AES(filename, key_file, save_to)
        elif command == 'exit':
            break


if __name__ == '__main__':
    main()
