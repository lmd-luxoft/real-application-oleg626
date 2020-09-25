# Copyright 2019 by Kirill Kanin.
# All rights reserved.

import os
import typing
import datetime
import server.utils as utils
from collections import OrderedDict
from server.crypto import BaseCipher, AESCipher, RSACipher, HashAPI


class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class FileService(metaclass=SingletonType):
    """Singleton class with methods for working with file system.

    """
    __path = "C:/work/training"

    def __init__(self):
        print('File service initialized')

    @property
    def path(self) -> str:
        """Working directory path getter.

        Returns:
            Str with working directory path.

        """
        return self.__path

    @path.setter
    def path(self, value: str):
        """Working directory path setter.

        Args:
            value (str): Working directory path.

        """
        self.__path = value

    def change_dir(self, path: str):
        """Change current directory of app.

        Args:
            path (str): Path to working directory with files.

        Raises:
            AssertionError: if directory does not exist.

        """
        try:
            assert os.path.exists(path), "Path doesn't exist"

            os.chdir(path)
            self.path = os.getcwd()

        except AssertionError as msg:
            print(msg)

    def get_file_data(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            ValueError: if security level is invalid.

        """
        filename_with_txt = filename + '.txt'
        try:
            assert os.path.isfile(filename_with_txt), "File doesn't exist"
            create_date = os.path.getctime(filename_with_txt)
            create_date = datetime.datetime.fromtimestamp(create_date).strftime('%Y-%m-%d %H:%M:%S')
            edit_date = os.path.getmtime(filename_with_txt)
            edit_date = datetime.datetime.fromtimestamp(edit_date).strftime('%Y-%m-%d %H:%M:%S')
            size = os.path.getsize(filename_with_txt)

            with open(filename_with_txt, 'r') as f:
                data = f.read()

            file_data = {'name': filename_with_txt, 'data': data, 'create date': create_date, 'edit date': edit_date,
                         'size': size}
            return file_data
        except AssertionError as msg:
            print(msg)

    async def get_file_data_async(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file. Asynchronous version.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            ValueError: if security level is invalid.

        """

        pass

    @staticmethod
    def get_files() -> typing.List[typing.Dict[str, str]]:
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
                files_data.append({'name': file, 'create date': create_date, 'edit date': edit_date, 'size': size})
        return files_data

        pass

    def create_file(self, filename : str, content: str = None,
                          security_level: str = None, user_id: int = None) -> typing.Dict[str, str]:
        """Create new .txt file.

        Method generates name of file from random string with digits and latin letters.

        Args:
            filename (str): Name of the file
            content (str): String with file content,
            security_level (str): String with security level,
            user_id (int): User Id.

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
        try:
            assert not os.path.exists(filename_with_txt), "File already exists"

            with open(filename_with_txt, 'w') as f:
                f.write(content)

            return FileService.get_file_data(self, filename)

        except AssertionError as msg:
            print(msg)

    @staticmethod
    def delete_file(filename: str):
        """Delete file.

        Args:
            filename (str): Filename without .txt file extension.

        Returns:
            Str with filename with .txt file extension.

        Raises:
            AssertionError: if file does not exist.

        """
        filename_with_txt = filename + ".txt"
        try:
            assert os.path.isfile(filename_with_txt), "File doesn't exist"
            os.remove(filename_with_txt)

            return filename_with_txt
        except AssertionError as msg:
            print(msg)


class FileServiceSigned(FileService):
    """Singleton class with methods for working with file system and file signatures.

    """
    def get_file_data(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid, signatures are not match,
            signature file does not exist,
            ValueError: if security level is invalid.

        """
        file_data = super(FileServiceSigned, self).get_file_data(filename, user_id)
        raw_string = "_".join([str(x) for x in list(file_data.values())])
        actual_hash = HashAPI.hash_md5(raw_string)
        try:
            assert os.path.isfile(filename+'.md5'), "Signature doesn't exist"
            with open(filename + '.md5') as md5:
                expected_hash = md5.read()
            assert actual_hash == expected_hash, "Hash doesn't match"
            return file_data
        except AssertionError as msg:
            print(msg)

    async def get_file_data_async(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file. Asynchronous version.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid, signatures are not match,
            signature file does not exist,
            ValueError: if security level is invalid.

        """

        pass

    def create_file(self, filename: str, content: str = None,
                    security_level: str = None, user_id: int = None) -> typing.Dict[str, str]:
        """Create new .txt file with signature file.

        Method generates name of file from random string with digits and latin letters.

        Args:
            filename (str): Name of the file
            content (str): String with file content,
            security_level (str): String with security level,
            user_id (int): User Id.

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
        super(FileServiceSigned, self).create_file(filename, content, security_level, user_id)
        file_data = super(FileServiceSigned, self).get_file_data(filename)
        raw_string = "_".join([str(x) for x in list(file_data.values())])
        hashed_string = HashAPI.hash_md5(raw_string)
        with open(filename+'.md5', 'w') as md5:
            md5.write(hashed_string)
        return file_data

    def delete_file(self, filename: str):
        """Delete file.

        Args:
            filename (str): Filename without .txt file extension.

        Returns:
            Str with filename with .txt file extension.

        Raises:
            AssertionError: if file does not exist.
        """
        super(FileServiceSigned, self).delete_file(filename)

        try:
            filename_md5 = filename + '.md5'
            assert os.path.isfile(filename_md5), "md5 doesn't exist"
            os.remove(filename_md5)

            return filename_md5
        except AssertionError as msg:
            print(msg)
