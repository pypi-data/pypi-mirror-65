import os

from flash_handler.config import Config


class FileKeeper(object):
    """文件“管家”。管理工作目录下的Excel文件列表和全部文件的列表。每个文件都有自己的索引。可用
    该索引获取文件名和文件路径，并进行相关操作。

    注意：索引的值是从1开始的整数。
    """
    EXCEL_SUFFIX = 'xlsx'

    def __init__(self, dir_path):
        super().__init__()
        self.dir_path = dir_path

        self._all_files = None
        self._excel_files = None

    def _refresh(self):
        """更新全体文件列表和excel文件列表。

        注：同时更新两者，避免两者在逻辑上不一致。"""
        file_names = [name for name in os.listdir(self.dir_path)]
        indexes = range(1, 1 + len(file_names))  # 索引值从1开始，避免加减1转化

        self._all_files = dict(zip(indexes, file_names))
        self._excel_files = {index: name
                             for index, name in self._all_files.items()
                             if name.endswith(self.EXCEL_SUFFIX)}

    @property
    def all_files(self):
        """全部文件的列表。字典类型：键为索引，值为文件名。"""
        self._refresh()
        return self._all_files

    @property
    def excel_files(self):
        """全部Excel文件的列表。字典类型：键为索引，值为文件名。"""
        self._refresh()
        return self._excel_files

    def get_file_path(self, index):
        """根据文件索引index，获取文件的路径。"""
        try:
            file_name = self.all_files[index]
        except IndexError:
            return None

        return os.path.join(self.dir_path, file_name)

    def print_excel_files(self, indexes=None):
        """打印所有Excel文件。可选参数indexes是文件索引，可以用于选择要打印的文件。"""
        self.print_files(self.excel_files, indexes=indexes)

    def print_all_files(self):
        """打印所有文件。"""
        self.print_files(self.all_files)

    @staticmethod
    def print_files(files, indexes=None):
        """根据索引indexes打印所有文件。"""
        if indexes is None:
            indexes = sorted(files.keys())

        for i, index in enumerate(indexes):
            print(index, files[index], end='\t')
            if 0 == (i + 1) % 4:
                print()
        print()


FILE_KEEPER = None
if FILE_KEEPER is None:
    FILE_KEEPER = FileKeeper(Config.DIR_PATH)
