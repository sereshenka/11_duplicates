import os
 
def list_of_all_files(root_dir):
    diction = {}
    for dirName, subdirList, fileList in os.walk(root_dir):
        for fname in fileList:
            path = os.path.join(dirName, fname)
            size = os.path.getsize(path)
            if not size in diction:
                diction[size] = [fname]
            else :
                fname = ['%s' %fname]
                for value in diction.values():
                    if fname == value:
                        print(fname)
    return (diction)
#был также вариант,где все значения записывались в словарь(размер,имя,путь) и потом шло сравнение
## вначале размера,потом имен,а потом ,если сходилось и находился дубликат предлагалось выбрать,
## какой фаил удалить(для этого и нужен был путь к фаилу)

def are_files_duplicates(file_path1, file_path_2):
    pass


if __name__ == '__main__':
    root_dir = input ('Укажите папку:')
    diction = list_of_all_files(root_dir)
    srav(root_dir,diction)
