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
    try:
        numbers = input('Введите номера фаилов(через запятую),чтобы удалить их.'
                        'Чтобы выйти сочетание клавиш(ctrl+c)\n').split(',')
    except KeyboardInterrupt:
        return None
    except EOFError:
        return None
    return numbers
   

def print_delete_information(delete_error, duplicates):
    if delete_error != []:
        for number in delete_error:
            print('Ошибка в удалении файла(возможно его ' \
                    'не существует)', duplicates[number]) 
    else:
        print ('Удаление фаилов прошло успешно')


def process_of_deleting_files(integer_numbers, duplicates):
    delete_error = []
    for number in integer_numbers:
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


def is_folder_path_valid(folder_path):
    folder_errors = []
    if folder_path is None:
        folder_errors.append('Не введен путь')
        return False, folder_errors
    if not os.path.exists(folder_path):
        folder_errors.append('Папки не существует')
        return False, folder_errors
    return True, folder_errors


def work_with_duplicates():
    duplicates_errors = []
    
    duplicates_dictionary = create_duplicate_dictionary(folder_path)
    if duplicates_dictionary == {}:
        duplicates_errors.append('Нет файлов в каталогах и подкаталогах')
        return None, duplicates_errors
    
    duplicates = filter_duplicates(duplicates_dictionary)
    if duplicates == []:
        duplicates_errors.append('Дубликатов в данном каталоге,'
                                 'а также подкаталогах нет.')
        return None, duplicates_errors
    
    print_duplicates(duplicates)
    return duplicates, None

def get_integer_number(numbers):
    try:
        integer_numbers = list(map(int, numbers))
    except ValueError:
        return None
    return integer_numbers

    
if __name__ == '__main__':
    folder_path = input_direction()
    is_valid, folder_errors = is_folder_path_valid(folder_path)
    if not is_valid:
        print(folder_errors)
        exit()
        
    duplicates, duplicates_errors = work_with_duplicates()
    if not duplicates:
        print(duplicates_errors)
        exit()

    numbers = input_of_numbers()
    if numbers is None:
        exit()
    integer_numbers = get_integer_number(numbers)
    if integer_numbers is None:
        print('Введены не числа\Не было введено ни одного числа')
        exit()
        
    delete_error = process_of_deleting_files(integer_numbers, duplicates)       
    print_delete_information(delete_error, duplicates)
