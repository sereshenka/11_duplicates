#!/usr/bin/python
#-*- coding: utf-8 -*-


import os
import sys
import argparse
from collections import defaultdict


def load_win_unicode_console():
    if sys.platform == 'win32':
        import win_unicode_console
        win_unicode_console.enable()


def read_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', help='Укажите путь к файлу ', nargs = '?')
    file_path = parser.parse_args().folder
    return (existence_of_arguments(file_path, parser))


def existence_of_arguments(file_path, parser):
    if not file_path:
        parser.print_help()
        return None
    else:
        return (file_path)   
                            

def find_duplicates(duplicates_dictionary):
    duplicates_dictionary = list(filter(lambda x: len(x) > 1,duplicates_dictionary.values()))
    duplicates = [duplicate for duplicates in duplicates_dictionary for duplicate in duplicates]
    return (duplicates)


def create_duplicate_dictionary(folder):
    duplicates_dictionary = defaultdict(list)
    for directory, sub_dirs, files in os.walk(folder):
        for file_name in files:
            path = os.path.join(directory, file_name)
            size = os.path.getsize(path)
            duplicates_dictionary[file_name,size].append(path)
    return (duplicates_dictionary)


def input_of_numbers():
    try:
        numbers = input('Введите номера фаилов,чтобы удалить их.'
                    'Чтобы выйти сочетание клавиш(ctrl+c)\n').split(',')
        for number in numbers:
            int(number)
    except ValueError:
        numbers = None
        print('Введены не числа\Не было введено ни одного числа')
    except KeyboardInterrupt:
        numbers = None
    return (numbers)


def delete_files(numbers,duplicates):
    for number in numbers:
        try:
            os.remove(duplicates[int(number)])
            print ('Удаление фаила прошло успешно', duplicates[int(number)])
        except OSError:
            print('Ошибка в удалении файла(возможно его ' \
                  'не существует)', duplicates[int(number)])


def print_duplicates(duplicates):
    print('Следующие фаилы явлются дубликатами:')
    for duplicate in enumerate(duplicates):
        print(duplicate)
    

if __name__ == '__main__':
    load_win_unicode_console()
    folder = read_arguments()
    if folder is not None:
        duplicates_dictionary = create_duplicate_dictionary(folder)
        duplicates = find_duplicates(duplicates_dictionary)
        print_duplicates(duplicates)
        numbers = input_of_numbers()
        if numbers is not None:
            delete_files(numbers,duplicates)
