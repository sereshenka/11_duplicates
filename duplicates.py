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
    """
    использую с join,чтобы программа работала при указании пути,в котором папка
    может содержать в названии пробел.(C:\\Users\\New User\\file.format)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', help='Укажите путь к папке ', nargs = '+')
    arguments = parser.parse_args().folder
    try :
        file_path = ' '.join(arguments)
    except TypeError:
        return None, parser
    return file_path, parser


def create_duplicate_dictionary(folder):
    duplicates_dictionary = defaultdict(list)
    for directory, sub_dirs, files in os.walk(folder):
        for file_name in files:
            path = os.path.join(directory, file_name)
            size = os.path.getsize(path)
            duplicates_dictionary[file_name,size].append(path)
    return duplicates_dictionary

                            
def find_duplicates(duplicates_dictionary):
    duplicates_dictionary = list(filter(lambda x: len(x) > 1,duplicates_dictionary.values()))
    duplicates = [duplicate for duplicates in duplicates_dictionary for duplicate in duplicates]
    return duplicates


def input_of_numbers():
    numbers = input('Введите номера фаилов(через запятую),чтобы удалить их.'
                    'Чтобы выйти сочетание клавиш(ctrl+c)\n').split(',')
    for number in numbers:
        int(number)
    return numbers
   

def print_delete_information(numbers,duplicates):
    for number in numbers:
        remove = delete_files(number,duplicates)
        if remove is None:
            print('Ошибка в удалении файла(возможно его ' \
                  'не существует)', duplicates[int(number)]) 
        else:
            print ('Удаление фаила прошло успешно', duplicates[int(number)])


def delete_files(number,duplicates):
    try:
        os.remove(duplicates[int(number)])
        return True
    except OSError:
        return None


def print_duplicates(duplicates):
    print('Следующие фаилы явлются дубликатами:')
    for duplicate in enumerate(duplicates):
        print(duplicate)


if __name__ == '__main__':
    while True:
        load_win_unicode_console()
        
        folder, parser = read_arguments()
        if folder is None:
            parser.print_help()
            break
        if not os.path.exists(folder):
            print('Папки не существует')
            break
        
        duplicates_dictionary = create_duplicate_dictionary(folder)
        if duplicates_dictionary == {}:
            print('Нет файлов в каталогах и подкаталогах')
            break
        
        duplicates = find_duplicates(duplicates_dictionary)
        if duplicates == []:
            print('Дубликатов в данном каталоге,а также подкаталогах нет.')
            break
        print_duplicates(duplicates)

        try:
            numbers = input_of_numbers()
        except ValueError:
            print('Введены не числа\Не было введено ни одного числа')
            break
        except KeyboardInterrupt:
            break
        
        print_delete_information(numbers,duplicates)
        break
