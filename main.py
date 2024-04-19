import sys
import os
import shutil
from pathlib import Path

from normalize import normalize
import logging
from my_logger import get_logger

# logging into file and console
logger = get_logger('my_logger', logging.DEBUG)

# define path to the folder through the terminal
path_to_folder = sys.argv[1]
PATH = Path(path_to_folder)

# predefined folders and extensions
FOLDERS = {
    "images": ['JPEG', 'PNG', 'JPG', 'SVG'],
    "videos": ['AVI', 'MP4', 'MOV', 'MKV'],
    "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'XLS', 'CSV'],
    "music": ['MP3', 'OGG', 'WAV', 'AMR'],
    "archives": ['ZIP', 'GZ', 'TAR'],
    "unknowns": []
}


def create_folders(path):
    """
    Create predefined folders in the given path
    """
    for folder in FOLDERS:
        if not os.path.exists(os.path.join(path, folder)):
            os.makedirs(os.path.join(path, folder))


def sort_files(path):
    """
    Sorts the files in a folder
    """
    # normalize file names
    for root, folders, files in os.walk(path, topdown=False):
        for file in files:
            file_extension = file.split('.')[-1]
            file_name = file.split('.')[0]
            file_path = os.path.join(root, file)
            normalized_file_name = normalize(file_name)
            normalized_file_path = os.path.join(root, normalized_file_name + '.' + file_extension)
            os.rename(file_path, normalized_file_path)
            old_name = file_name + '.' + file_extension
            new_name = normalized_file_name + '.' + file_extension
            if old_name != new_name:
                logger.info('{} was renamed to {}'.format(old_name, new_name))

    # sort files
    for root, folders, files in os.walk(path, topdown=False):
        for file in files:
            file_extension = file.split(".")[-1].upper()
            defined_folder = None
            folder_path = None

            for fol, extensions in FOLDERS.items():
                if file_extension in extensions:
                    defined_folder = fol
                    folder_path = os.path.join(path, fol)
                    break

            if defined_folder:
                defined_file_path = os.path.join(folder_path, file)
            else:
                defined_file_path = os.path.join(path, 'unknowns', file)

            if (root != folder_path and root != os.path.join(path, 'unknowns')
                    and os.path.join(path, 'archives') not in root):
                try:
                    os.rename(os.path.join(root, file), defined_file_path)
                    logger.warning("This file was moved: {}".format(file))
                except OSError:
                    logger.error("This file was not moved: {}".format(file))
                    continue

    # delete empty folders
    for root, folders, files in os.walk(path, topdown=False):
        for folder in folders:
            if folder not in FOLDERS.keys() and not os.listdir(root + '/' + folder):
                os.rmdir(root + '/' + folder)
                logger.warning('Empty directory {} was deleted'.format(folder))


def show_list_of_files(path):
    """
    Shows the list of files and extensions in the given path
    """
    # show list of files for each folder
    for folder in os.listdir(path):
        if folder != 'archives':
            list_of_files = os.listdir(os.path.join(path, folder))
            logger.info('List of files in {}: {}'.format(folder, list_of_files))
        elif folder == 'archives':
            for root, folders, files in os.walk(os.path.join(path, folder), topdown=False):
                list_of_archives = [file for file in files]
                logger.info('List of files in archives: {}'.format(list_of_archives))

    # show list of known and unknown extensions
    known_extensions = []
    unknown_extensions = []
    for root, folders, files in os.walk(path, topdown=False):
        if root != os.path.join(path, 'unknowns'):
            known_extensions.extend([file.split('.')[-1].upper() for file in files])
        else:
            unknown_extensions.extend([file.split('.')[-1].upper() for file in files])

    logger.info('Known extensions: {}'.format(set(known_extensions)))
    logger.info('Unknown extensions: {}'.format(set(unknown_extensions)))


def unzip_archives(path):
    """
    Unzips archives in the given path
    """
    archives_path = os.path.join(path, 'archives')
    for item in os.listdir(archives_path):
        if item.split('.')[-1].upper() in FOLDERS['archives']:
            item_new_folder = os.path.join(archives_path, os.path.splitext(item)[0])
            item_old_path = os.path.join(archives_path, item)
            logger.info(f'Unzipping {item}')
            shutil.unpack_archive(item_old_path, item_new_folder)
    for item in os.listdir(archives_path):
        if item.split('.')[-1].upper() in FOLDERS['archives']:
            item_old_path = os.path.join(archives_path, item)
            os.remove(item_old_path)


if __name__ == '__main__':
    create_folders(PATH)
    sort_files(PATH)
    unzip_archives(PATH)
    show_list_of_files(PATH)









