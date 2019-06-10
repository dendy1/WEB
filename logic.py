import os

BASE_DIR = "images/icons/"

class Counter:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1

class PseudoDirEntry:
    def __init__(self, path):
        if not path:
            self.path = ''
        else:
            self.path = os.path.normpath(path)

        self.name = os.path.basename(self.path)

        if not self.name:
            self.name = self.path

        self._is_file = os.path.isfile(self.path)

        self.directories = self.path.split(os.sep)
        if self.directories[0]:
            self.directories[0] += os.sep

        if path:
            self._access = os.access(self.path, os.R_OK | os.X_OK)

    @property
    def previous_path(self):
        return self.__previous_path_h(len(self.directories) - 1)

    @property
    def breadcrumbs(self):
        breadcrumbs = []

        for i in range(len(self.directories)):
            url = self.__previous_path_h(i + 1)
            text = self.directories[i]
            breadcrumbs.append((url, text))

        return breadcrumbs

    @property
    def is_file(self):
        return self._is_file

    @property
    def icon(self):
        if self.is_file:
            ext = os.path.splitext(self.name)[1]

            if not self.access:
                return BASE_DIR + "file_ad.png"

            return BASE_DIR + ext.lstrip(".") + ".png"
        else:
            if not self.access:
                return BASE_DIR + "folder_ad.png"

            return BASE_DIR + "folder.png"

    @property
    def default_icon(self):
        if self.is_file:
            if not self.access:
                return BASE_DIR + "file_ad.png"

            return BASE_DIR + "file.png"
        else:
            if not self.access:
                return BASE_DIR + "folder_ad.png"

            return BASE_DIR + "folder.png"

    @property
    def access(self):
        return self._access

    def __previous_path_h(self, index):
        path = ""
        for i in range(index):
            path = os.path.join(path, self.directories[i])
        return path

def get_drives_letters():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives = ['%s:\\' % d for d in letters if os.path.exists('%s:' % d)]
    return drives

def search_in_dir(name, path):
    if not path:
        drives = get_drives_letters()
        for drive in drives:
            yield from search_in_dir(name, drive)

    #"filename" "fol.der" -> точный поиск папок и файлов
    #filename -> поиск папок и файлов по вхождению запроса в название
    #*.ext -> поиск всех файлов и заданным расширением
    #filename.ext -> поиск файлов по названию и расширению

    #filename.ext == filename + .ext

    try:
        for element in os.scandir(path):
            new_name = name.strip("\"")

            if name.startswith("\"") and name.endswith("\""):
                if '.' in new_name:
                    if new_name == element.name:
                        yield PseudoDirEntry(element.path)
                elif new_name == os.path.splitext(element.name)[0]:
                    yield PseudoDirEntry(element.path)

            elif new_name.startswith("*"):
                new_name = new_name.lstrip("*")
                if new_name == os.path.splitext(element.name)[1]:
                    yield PseudoDirEntry(element.path)

            elif '.' in new_name:
                if new_name in element.name:
                    yield PseudoDirEntry(element.path)

            else:
                if new_name in element.name:
                    yield PseudoDirEntry(element.path)

            yield from search_in_dir(name, element.path)

    except PermissionError:
        pass
        #print("Permission Error",file=sys.stderr)
    except FileNotFoundError:
        pass
        #print("FileNotFound Error",file=sys.stderr)
    except NotADirectoryError:
        pass
        #print("NotADirectory Error",file=sys.stderr)

def my_scan_dir(path):
    for element in os.scandir(path):
        yield PseudoDirEntry(element.path)

def get_files_count(directory):
    c = Counter()
    __get_files_count_help(directory, c)
    return c.counter

def __get_files_count_help(directory, counter):
    for element in os.scandir(directory):
        counter.increment()

        if not element.is_file():
            __get_files_count_help(element.path, counter)