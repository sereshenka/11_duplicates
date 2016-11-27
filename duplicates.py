#!/usr/bin/python

import os
import sys
import argparse
from collections import defaultdict


def load_win_unicode_console():
    if sys.platform == 'win32':
        import win_unicode_console
        win_unicode_console.enable()


def input_direction():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Укажите путь к папке ', nargs = '?')
    direction = parser.parse_args().path
    if direction is None:
        parser.print_help()
    return direction


def create_duplicate_dictionary(direction):
    duplicates_dictionary = defaultdict(list)
    for directory, sub_dirs, files in os.walk(direction):
        for file_name in files:
            path = os.path.join(directory, file_name)
            size = os.path.getsize(path)
            duplicates_dictionary[file_name,size].append(path)
    return duplicates_dictionary

                            
def filter_duplicates(duplicates_dictionary):
    duplicates_dictionary_with_lenght_over_1 = list(filter(lambda x: \
                            len(x) > 1,duplicates_dictionary.values()))
    duplicates = [duplicate for duplicate_dictionary in \
                  duplicates_dictionary_with_lenght_over_1 \
                  for duplicate in duplicate_dictionary]
    return duplicates


def input_of_numbers():
    numbers = input('Введите номера фаилов(через запятую),чтобы удалить их.'
                    'Чтобы выйти сочетание клавиш(ctrl+c)\n').split(',')
    for number in numbers:
        number = int(number)
    return numbers
   

def print_succes_or_not_process_of_deleting_files(numbers,duplicates):
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
    for indx, duplicate in enumerate(duplicates):
        print(indx+1,duplicate)


if __name__ == '__main__':
    while True:
        load_win_unicode_console()
        direction = input_direction()
        if direction is None:
            break
        if not os.path.exists(direction):
            print('Папки не существует')
            break
        
        duplicates_dictionary = create_duplicate_dictionary(direction)
        if duplicates_dictionary == {}:
            print('Нет файлов в каталогах и подкаталогах')
            break
        
        duplicates = filter_duplicates(duplicates_dictionary)
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
        
        print_succes_or_not_process_of_deleting_files(numbers,duplicates)
        break
