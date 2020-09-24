# Copyright 2019 by Kirill Kanin.
# All rights reserved.

import argparse
import os
import sys
import logging
import json
from aiohttp import web
from server.handler import Handler
#from server.database import DataBase
from server.file_service import FileService, FileServiceSigned
import server.file_service_no_class as FileServiceNoClass


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
    files = FileService().get_files()
    return files

def get_file_data(filename):
    """Get full info about file.

    Args:
        path (str): Working directory path.

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
    assert os.path.exists(filename), ("File doesn't exist")

    file_data = FileService().get_file_data(filename)
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

    return FileService().create_file(file_name, file_content)



def delete_file(filename):
    """Delete file.

    Args:
        filename (str): File to delete without .txt extension

    Returns:
        Str with filename with .txt file extension.

    Raises:
        AssertionError: if file does not exist.

    """
    return FileService().delete_file(filename)


def change_dir(path):
    """Change working directory.

    Args:
        path (str): Working directory path.

    Returns:
        Str with successfully result.

    """
    FileService().change_dir(path)

def summ(a: int, b: int):
    return a+b

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
    change_dir(args.directory)
    

if __name__ == '__main__':
    main()
