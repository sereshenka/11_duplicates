#!/usr/bin/python


import os
import sys
import argparse
from collections import defaultdict


def input_direction():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Укажите путь к папке ', nargs = '?')
    folder_path = parser.parse_args().path
    if folder_path is None:
        parser.print_help()
    return folder_path


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
    return numbers
   

def print_delete_information(delete_error, duplicates):
    if delete_error != []:
        for number in delete_error:
            print('Ошибка в удалении файла(возможно его ' \
                    'не существует)', duplicates[number]) 
    else:
        print ('Удаление фаилов прошло успешно')


def process_of_deleting_files(numbers, duplicates):
    delete_error = []
    for number in numbers:
        number-=1
        try:
            os.remove(duplicates[number])
        except OSError:
            delete_error.append(number)
    return  delete_error


def print_duplicates(duplicates):
    print('Следующие фаилы явлются дубликатами:')
    for indx, duplicate in enumerate(duplicates):
        print(indx+1, duplicate)


if __name__ == '__main__':
    while True:
        folder_path = input_direction()
        if folder_path is None:
            break
        if not os.path.exists(folder_path):
            print('Папки не существует')
            break
        
        duplicates_dictionary = create_duplicate_dictionary(folder_path)
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
        except KeyboardInterrupt:
            break
        try:
            numbers = list(map(int, numbers))
        except ValueError:
            print('Введены не числа\Не было введено ни одного числа')
            break
        
        delete_error = process_of_deleting_files(numbers, duplicates)       
        print_delete_information(delete_error, duplicates)
        break
