import os
import sys
import argparse
from collections import defaultdict


def input_direction():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Укажите путь к папке ',
                        nargs = '?', required = True)
    folder_path = parser.parse_args().path
    return folder_path


def create_files_dictionary(direction):
    files_dictionary = defaultdict(list)
    for directory, sub_dirs, files in os.walk(direction):
        for file_name in files:
            path = os.path.join(directory, file_name)
            size = os.path.getsize(path)
            files_dictionary[file_name,size].append(path)
    return files_dictionary

                            
def filter_files(files_dictionary):
    duplicates_dictionary = filter(lambda x: len(x) > 1,
                                   files_dictionary.values())
    duplicates = [duplicate for duplicate_dictionary in duplicates_dictionary 
                  for duplicate in duplicate_dictionary]
    return duplicates
   

def print_duplicates(duplicates):
    print('Следующие фаилы явлются дубликатами:')
    for indx, duplicate in enumerate(duplicates):
        print(indx+1, duplicate)


if __name__ == '__main__':
    folder_path = input_direction()
    if not os.path.exists(folder_path):
        print('Папки не существует')
        exit()
    files_dictionary = create_files_dictionary(folder_path)
    if not files_dictionary:
        print('Нет файлов в каталогах и подкаталогах')
        exit()
    duplicates = filter_files(files_dictionary)
    if not duplicates:
        print('Дубликатов в данном каталоге, а также подкаталогах нет')
        exit()
    print_duplicates(duplicates)
