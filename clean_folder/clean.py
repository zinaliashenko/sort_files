import logging
import os
import pathlib
import re
import shutil
import sys

logging.basicConfig(filename='sort.log',
                    filemode='w',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d.%m.%Y %I:%M:%S %p',
                    level=logging.DEBUG)

PATH = sys.argv[1]

FOLDERS = {'documents': ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX', '.RTF'],
           'images': ['.JPEG', '.PNG', '.JPG', '.SVG', '.BMP'],
           'audio': ['.MP3', '.OGG', '.WAV', '.AMR'],
           'video': ['.AVI', '.MP4', '.MOV', '.MKV'],
           'archives': ['.ZIP', '.GZ', '.TAR']}


def change_the_name(path=PATH):

    list_dir_and_files = os.listdir(path)

    for name in list_dir_and_files:
        name_path = os.path.join(path, name)

        if os.path.isdir(name_path):
            new_dir_name = normalize(name)
            if name == new_dir_name:
                continue
            os.rename(name_path, fr'{path}\{new_dir_name}')
            print(name, 'was renamed as ', new_dir_name)

        if os.path.isfile(name_path):
            new_file_name = normalize(os.path.splitext(name)[0])
            if name == new_file_name + os.path.splitext(name)[1]:
                continue
            new_file_name = new_file_name + os.path.splitext(name)[1]
            os.rename(name_path, fr'{path}\{new_file_name}')
            print(name, 'was renamed as ', new_file_name)

    for name in list_dir_and_files:
        name_path = os.path.join(path, name)
        if os.path.isdir(name_path):
            change_the_name(name_path)


def create_folders(path=PATH):

    for key in FOLDERS.keys():
        for key in FOLDERS.keys():
            folder_path = os.path.join(path, key)
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
                print(key, 'is made')
                logging.info(f'{key} is made')


def delete_empty_folder(path=PATH):

    for item in os.listdir(path):
        if FOLDERS.get(item):
            continue

        dir_path = os.path.join(path, item)

        if os.path.isdir(dir_path):
            delete_empty_folder(dir_path)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(dir_path, 'DELETED')
                logging.info(f'{dir_path} DELETED')


def get_the_info(path=PATH):

    for key in FOLDERS.keys():
        list_of_files = os.listdir(os.path.join(PATH, key))
        if list_of_files != []:
            print(f'List of files in {key}: {list_of_files}')

    list_folders_and_files = walk_the_directory(path)
    known_extentions = []
    unknown_extentions = []

    for item in list_folders_and_files:
        file_ext = os.path.splitext(item)[1]  # .txt

        for key in FOLDERS.keys():
            if os.path.isfile and file_ext:  # not []
                if file_ext.upper() in FOLDERS[key]:
                    known_extentions.append(file_ext)
                if not file_ext.upper() in FOLDERS[key]:
                    unknown_extentions.append(file_ext)

    print('Known extentions: ', set(known_extentions))  # unique
    print('Unknown extentions: ', set(unknown_extentions))


def normalize(file_name):

    CYRILLIC = ('а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і',
                'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
                'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ю', 'я', 'А', 'Б', 'В',
                'Г', 'Ґ', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І', 'Ї', 'Й', 'К',
                'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц',
                'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я')

    LATIN = ('a', 'b', 'v', 'g', 'g', 'd', 'e', 'e', 'zh', 'z', 'y', 'i',
             'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
             'f', 'h', 'c', 'ch', 'sh', 'shch', '', 'yu', 'ya', 'A', 'B', 'V',
             'G', 'G', 'D', 'E', 'e', 'Zh', 'Z', 'I', 'I', 'Yi', 'Y', 'K',
             'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F', 'Ch', 'c',
             'Ch', 'Sh', 'Shch', '', 'Yu', 'Ya')

    TRANSLIT_DICT = {}

    for c, l in zip(CYRILLIC, LATIN):
        TRANSLIT_DICT[ord(c)] = l

    latin_name = file_name.translate(TRANSLIT_DICT)
    new_file_name = re.sub('[^a-zA-Z.0-9_]', '_', latin_name)

    return new_file_name


def sort_the_files(list_folders_and_files):

    for file_name in list_folders_and_files:
        if os.path.isdir(file_name):
            continue

        file_ext = pathlib.Path(file_name).suffix.upper()
        for key in FOLDERS.keys():
            if file_ext in FOLDERS[key]:

                destination_path = os.path.join(PATH, key)
                if file_name.startswith(destination_path):
                    break

                try:
                    shutil.move(file_name, destination_path)
                    print(f'File {file_name} was moved to {key}')
                    logging.info(f'File {file_name} was moved to {key}')
                except shutil.Error:
                    print(
                        f'File with this name {file_name} is already in {key} folder')
                    logging.warning(
                        f'File with this name {file_name} is already in {key} folder')


def unpack_archives(path):

    list_archives = os.listdir(path)
    for archive in list_archives:
        archive_path = os.path.join(path, archive)
        try:
            shutil.unpack_archive(
                archive_path, f'{os.path.splitext(archive_path)[0]}')
            logging.info(f'Archieve {archive} was unpacked')
            print(f'Archieve {archive} was unpacked')
            os.remove(archive_path)
        except shutil.ReadError:
            print('Archive', archive, 'has already been unpacked')
            logging.warning(f'Archive {archive} has already been unpacked')


def walk_the_directory(path=PATH):

    list_folders_and_files = []
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        list_folders_and_files.append(file_path)

        if os.path.isdir(file_path):
            list_folders_and_files += walk_the_directory(file_path)

    return list_folders_and_files


def main():
    
    create_folders(PATH)

    list_folders_and_files = walk_the_directory(PATH)

    sort_the_files(list_folders_and_files)

    delete_empty_folder(PATH)

    unpack_archives(fr'{PATH}\archives')

    change_the_name(PATH)

    get_the_info(PATH)


if __name__ == '__main__':

    main()