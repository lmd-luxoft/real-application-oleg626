# Copyright 2019 by Kirill Kanin.
# All rights reserved.


import os
import datetime
import sys
import server.utils as utils

extension = 'txt'


def change_dir(path):
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.

    Raises:
        AssertionError: if directory does not exist.

    """
    assert os.path.exists(path), ("Path doesn't exist")

    os.chdir(path)
    print("Current location", os.getcwd())


def get_file_data(filename):
    """Get full info about file.

    Args:
        filename (str): Filename without .txt file extension.

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
    filename_with_txt = filename + '.txt'
    create_date = os.path.getctime(filename_with_txt)
    create_date = datetime.datetime.fromtimestamp(create_date).strftime('%Y-%m-%d %H:%M:%S')
    edit_date = os.path.getmtime(filename_with_txt)
    edit_date = datetime.datetime.fromtimestamp(edit_date).strftime('%Y-%m-%d %H:%M:%S')
    size = os.path.getsize(filename_with_txt)

    with open(filename_with_txt, 'r') as f:
        data = f.read()

    file_data = {'name': filename_with_txt, 'data': data, 'create date': create_date, 'edit date': edit_date, 'size': size}
    return file_data


def get_files():
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
            name (str): name of file with .txt extension.
            create_date (str): date of file creation.
            edit_date (str): date of last file modification.
            size (str): size of file in bytes.

    """
    list_of_files = os.listdir()
    files_data = []
    for file in list_of_files:
        if os.path.isfile(file):
            create_date = os.path.getctime(file)
            create_date = datetime.datetime.fromtimestamp(create_date).strftime('%Y-%m-%d %H:%M:%S')
            edit_date = os.path.getmtime(file)
            edit_date = datetime.datetime.fromtimestamp(edit_date).strftime('%Y-%m-%d %H:%M:%S')
            size = os.path.getsize(file)
            files_data.append({'name' : file, 'create date': create_date, 'edit date' : edit_date, 'size': size})
    return files_data



def create_file(filename, content=None, security_level=None):

    """Create new .txt file.


    Method generates name of file from random string with digits and latin letters.

    Args:
        filename (str): Name of the file without .txt extension
        content (str): String with file content,
        security_level (str): String with security level.

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
    filename_with_txt = filename + ".txt"
    assert not os.path.exists(filename_with_txt), ("File already exists")

    with open(filename_with_txt, 'w') as f:
        f.write(content)

    return get_file_data(filename)

def delete_file(filename):
    """Delete file.

    Args:
        filename (str): Filename without .txt file extension.

    Returns:
        Str with filename with .txt file extension.

    Raises:
        AssertionError: if file does not exist.

    """
    filename_with_txt = filename + ".txt"
    assert os.path.isfile(filename_with_txt), ("File doesn't exist")

    os.remove(filename_with_txt)

    return filename_with_txt

