import os

def get_drives():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives = ['%s:' % d for d in letters if os.path.exists('%s:' % d)]
    return drives

def search_in_directory(file_name, directory_name):
    try:
        for element in os.scandir(directory_name):
            if element.is_file():
                new_file_name = file_name.strip("\"")

                if new_file_name.startswith("*"):
                    new_file_name = new_file_name.lstrip("*")
                    if new_file_name == os.path.splitext(element.name)[1]:
                        yield file(directory_name, element.name)

                elif (file_name.startswith("\"") and file_name.endswith("\"")):
                    if new_file_name == os.path.splitext(element.name)[0]:
                        yield file(directory_name, element.name)

                else:
                    if new_file_name in element.name:
                        yield file(directory_name, element.name)
            else:
                yield from search_in_directory(file_name, element.path)
    except PermissionError:
        pass
    except NotADirectoryError:
        pass

def search_in_list(file_name, pathes):
    for path in pathes:
        elementName = path.name
        directoryName = path.directory

        new_file_name = file_name.strip("\"")

        if new_file_name.startswith("*"):
            new_file_name = new_file_name.lstrip("*")
            if new_file_name == os.path.splitext(elementName)[1]:
                yield file(directoryName, elementName)

        elif (file_name.startswith("\"") and file_name.endswith("\"")):
            if new_file_name == os.path.splitext(elementName)[0]:
                yield file(directoryName, elementName)

        else:
            if new_file_name in elementName:
                yield file(directoryName, elementName)

def __get_all_files_directory(directory):
    try:
        for element in os.scandir(directory):
            if element.is_file():
                yield file(directory, element.name)
            else:
                yield from __get_all_files_directory(element.path)
    except PermissionError:
        pass
    except NotADirectoryError:
        pass

def get_all_files():
    drives = get_drives()
    allFiles = []

    for driveLetter in drives:
        for path in __get_all_files_directory(driveLetter + "\\"):
            allFiles.append(path)

    return allFiles

def search_all_drives(file_name):
    drives = get_drives()

    for drive in drives:
        for path in search_in_directory(file_name, drive + "\\"):
            yield path

class file:
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name

    def __str__(self):
        return self.directory + '\\' + self.name