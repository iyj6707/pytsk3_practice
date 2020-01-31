import sys
import pytsk3 as tsk


class ExtractFile:
    def __init__(self, path):
        self.path = path
        self.img = tsk.Img_Info(self.path)
        self.fs = tsk.FS_Info(self.img)

    def print_info(self):
        print('{0}'.format(self.fs.info))

    def open_directory(self, path):
        directory = self.fs.open_dir(path)
        for f in directory:
            size = f.info.meta.size
            name = f.info.name.name.decode('utf-8')
            print('{0}, {1}'.format(size, name))
