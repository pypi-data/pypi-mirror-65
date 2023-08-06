#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import os


def recursive_glob(dir_name, ignore_hidden=True):
    """
    Returns a list of all files in directory including sub-directories.

    :param dir_name: Dir name to glob recursively on
    :type dir_name: str
    :param ignore_hidden: if to ignore hidden files (that start with '.')
    :type ignore_hidden: bool

    :return: list of all files in the dir_name
    :rtype: list of str
    """
    dir_files = []
    for root, dirs, files in os.walk(dir_name):
        for any_file in files:
            # Adds the files to dir_files in two cases:
            # 1. wants all files (including hidden files)
            # 2. does not want hidden files - adds all regular files
            if (ignore_hidden and not any_file.startswith('.')) or \
               (not ignore_hidden):
                dir_files.append(os.path.join(root, any_file))

            if len(dir_files) % 1000 == 0 and len(dir_files) > 0:
                print("{} files collected...".format(len(dir_files)))
    return dir_files


def save_file(content, file_base_name, extension, dest_dir="."):
    """
    This function saves the file content to the destination dir (defaulted to ".") as base_name + extension,
    but adds a counter if needed.

    :param content: the content of the file
    :type content: bytes
    :param file_base_name: the future file name without extension
    :type file_base_name: str
    :param extension: the file name extension (for example: 'xlsx')
    :type extension: str
    :param dest_dir: where to save the file
                     Default: current directory
    :type dest_dir: str

    :return: full file path file was saved to
    :rtype: str
    """
    file_name = "{name}.{extension}".format(name=file_base_name, extension=extension)
    counter = 0
    while os.listdir(dest_dir).count(file_name) != 0:
        counter += 1
        file_name = "{name}-{counter}.{extension}".format(
            name=file_base_name,
            counter=counter,
            extension=extension
        )
    full_file_path = os.path.join(dest_dir, file_name)
    with open(full_file_path, 'wb') as f:
        f.write(content)
    return full_file_path


def get_file_length(file_path):
    """
    This function gets a file path and returns its length without reading it

    :param file_path: path to return length of
    :type file_path: str
    :return: file length (in bytes)
    :rtype: int
    """
    with open(file_path, 'rb') as f:
        f.seek(0, 2)
        file_len = f.tell()
    return file_len
