import os
import re

import pandas as pd
# TODO(luran): 这个readline
try:
    import readline
except ImportError:
    import pyreadline as readline

from flash_handler.const import Const
from flash_handler.error import Error
from flash_handler.excel_processor import ExcelProcessor
from flash_handler.file_keeper import FILE_KEEPER
from flash_handler.log import logger
from flash_handler.utils import Utils


# 设置pandas参数，使之在打印data frames时，能正确地对包含中文数据的data frames进行对齐。
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


def _split(str_):
    """把用户输入的字符串按分隔符分割。"""
    return re.split(Const.DELIMETERS, str_)


def _to_index_list(file_indexes):
    """把用户输入的文件索引转化成索引列表。"""
    index_list = _split(file_indexes)
    try:
        return [int(index) for index in index_list]
    except ValueError:
        return []


def _print_headers(file_path, prompt=''):
    """打印位于file_path的Excel文件的表头。其中的prompt是打印在表头前的提示信息，默认
    为空。"""
    headers = ExcelProcessor.read_headers(file_path)
    print('%s%s' % (prompt, ', '.join(headers)))


def _check_column_exist(file_path, column):
    headers = ExcelProcessor.read_headers(file_path)
    try:
        headers.index(column)
    except ValueError:
        return False
    return True


def _print_match_detail(matches, primary_key, secondary_key):
    """打印以primary_key为主键、以secondary_key为次键的Excel查询结果的详细信息：查询命中的
    文件名和具体数据行。"""
    print()
    file_indexes = sorted(matches.keys())
    for file_index in file_indexes:
        file_name = FILE_KEEPER.excel_files[file_index]
        data_frame = matches[file_index]
        print('表%d-%s, %s %s 包含信息如下:' % (
            file_index, file_name, primary_key, secondary_key))
        print()
        print(data_frame.to_string(index=False))
        print('-' * 60)
        print()


def _print_match_summary(matches):
    """打印以primary_key为主键、以secondary_key为次键的Excel查询结果的概要信息：查询命中的
    文件索引和文件名。"""
    print('包含搜索结果的文件有:')
    file_indexes = sorted(matches.keys())
    for i, file_index in enumerate(file_indexes):
        file_name = FILE_KEEPER.excel_files[file_index]
        print(file_index, file_name, end='\t')
        if 0 == (i + 1) % 4:
            print()
    print()


def excel_search(primary_key, secondary_key=''):
    """以主键primary_key和次键secondary_key对Excel文件进行搜索。所需要的其它信息会要求用户
    进行输入。其中的secondary_key为可选参数，默认为空字符串。"""

    # 根据主次关键字查找excel文件，获得结果
    matches = {}
    for index in FILE_KEEPER.excel_files:
        file_path = FILE_KEEPER.get_file_path(index)

        df = ExcelProcessor.search(file_path, primary_key, secondary_key)
        if 0 == len(df):
            continue

        matches[index] = df

    _print_match_detail(matches, primary_key, secondary_key)
    _print_match_summary(matches)
    print()

    # TODO(luran): 教学代码要求，查询结果为空时，要返回None，而不是空字典。这是需求方提出的
    # 临时性需求，准备发布PyPi时应修正。
    if not matches:
        return None
    return matches


def excel_files():
    """打印工作目录下的Excel文件名。"""
    print()
    FILE_KEEPER.print_excel_files()
    print()


def excel_add(file_indexes):
    """向索引file_indexes指定的Excel文件添加新的一行数据。所需要的其它信息会要求用户进行
    输入。"""
    index_list = _to_index_list(file_indexes)
    if not index_list:
        return False

    # 打印表头
    file_path = FILE_KEEPER.get_file_path(index_list[0])
    _print_headers(file_path, prompt='需要输入的信息有: ')

    # 获取新增行的数据
    values = input('请按顺序输入增加的信息(使用逗号隔开)：')
    if len(values) == 0:
        logger.error('没有输入内容')
        return
    values = _split(values)

    # 插入新数据
    index_list = _to_index_list(file_indexes)
    for index in index_list:
        file_path = FILE_KEEPER.get_file_path(index)
        ExcelProcessor.append(file_path, values)
    print("已增加!")
    print()

    # 后续信息打印
    for index in index_list:
        name = FILE_KEEPER.excel_files[index]
        path = FILE_KEEPER.get_file_path(index)
        df = ExcelProcessor.read_all(path)
        Utils.print_table_df(index, name, df[-1:])


def excel_delete(matches, file_indexes):
    """根据查询结果，对索引file_indexes指定的Excel文件进行删除操作。所需要的其它信息会要求
    用户进行输入。"""
    if not matches:
        Error.empty_query_result()
        return

    # 打印文件列表，供用户选择删除操作的目标
    index_list = _to_index_list(file_indexes)
    FILE_KEEPER.print_excel_files(index_list)
    print()

    # 用户选择删除操作的目标
    file_names = ['\n【%s】' % FILE_KEEPER.excel_files[index]
                  for index in index_list]
    file_names = ''.join(file_names)

    prompt = '确定将搜索的行从:{}\n删除(是/否)：'.format(file_names)
    choice = Utils.choose(prompt, ['是', '否'])
    if choice is None or choice == '否':
        return

    # 执行删除操作
    for file_index in index_list:
        file_path = FILE_KEEPER.get_file_path(file_index)
        row_indexes = matches[file_index].index
        ExcelProcessor.delete(file_path, row_indexes)

    print("已删除")


def excel_headers(file_indexes, prompt='表格的表头是: '):
    """打印file_indexes指定的Excel文件中第1个文件的表头。其中的prompt是打印在表头前的提示
    信息。"""
    index_list = _to_index_list(file_indexes)
    if not index_list:
        return False

    file_path = FILE_KEEPER.get_file_path(index_list[0])
    _print_headers(file_path, prompt=prompt)
    return True


def excel_update(matches, file_indexes, column):
    """根据查询结果matches，对文件索引file_indexes指定的Excel文件的列进行更新。具体是哪个列
    由参数column决定。所需要的其它信息会要求用户进行输入。"""
    if not matches:
        Error.empty_query_result()
        return

    if len(_split(column)) > 1:
        print('只可输入单个表头')
        return

    new_value = input('需要将{}修改为(只可输入单个信息)：'.format(column))
    print()

    prompt = '确定将【{}】更改为【{}】(是/否)：'.format(column, new_value)
    choice = Utils.choose(prompt, ['是', '否'])
    if choice is None or choice == '否':
        print('已取消')
        return

    if 0 == len(file_indexes):
        print('请输入需要修改的表格编号')
        return

    file_path = FILE_KEEPER.get_file_path(int(file_indexes[0]))
    if not _check_column_exist(file_path, column):
        print('表头不存在：%s' % column)
        return

    for index in _to_index_list(file_indexes):
        data_frame = matches[index]

        try:
            column_index = list(data_frame.columns).index(column)
        except ValueError:
            continue

        file_path = FILE_KEEPER.get_file_path(index)
        row_indexes = list(data_frame.index)
        ExcelProcessor.update(file_path, row_indexes, column_index, new_value)

    print('已修改')


def auto_picture():
    """绘制图表。所需要的信息会要求用户进行输入。

    注：函数命名受到spring.py的限制"""
    type_repr = input('请选择图片类型（柱状图，饼图，折线图）：')
    type_ = Utils.to_chart_type(type_repr)
    if type_ is None:
        print('不支持的处理方式')
        return

    FILE_KEEPER.print_excel_files()
    print()

    file_indexes = input('请选择需要绘画%s的表格编号: ' % type_repr)
    file_index_list = _to_index_list(file_indexes)
    if 1 != len(file_index_list):
        print('请输入有且仅有1个编号')
        return

    file_index = file_index_list[0]
    file_path = FILE_KEEPER.get_file_path(file_index)
    _print_headers(file_path)

    headers = ExcelProcessor.read_headers(file_path)

    horizontal_axis = Utils.choose('请输入横轴列名：', headers)
    if horizontal_axis is None:
        return

    vertical_axis = Utils.choose('请输入竖轴列名：', headers)
    if vertical_axis is None:
        return

    method_repr = input('请输入对【%s】数据的处理方式(%s):' % (vertical_axis,
                        Utils.get_all_methods()))
    method = Utils.to_method_type(method_repr)
    if method is None:
        print('不支持的处理方式')
        return

    title = input('请输入%s的名称:' % type_repr)
    if Utils.is_empty(title):
        Error.empty_input()
        return

    output_path = os.path.join(FILE_KEEPER.dir_path, '%s.png' % title)
    ExcelProcessor.draw_chart(
        file_path, type_, horizontal_axis, vertical_axis,
        method, title, output_path)
    return output_path


def auto_email():
    """发送邮件。所需要的信息会要求用户进行输入。"""
    while True:
        print()
        from_mail = input('请输入发件人邮箱: ')
        if Utils.is_empty(from_mail):
            Error.empty_input()
            return

        auth_code = input('请输入授权码: ')
        if Utils.is_empty(auth_code):
            Error.empty_input()
            return

        to_mails = input('请输入收件人邮箱，多个用英文逗号隔开: ')
        if Utils.is_empty(to_mails):
            Error.empty_input()
            return

        cc_mails = input('请输入抄送人邮箱，多个用英文逗号隔开：')
        print()

        print("系统读取到以下文件:")
        FILE_KEEPER.print_all_files()
        print()

        file_indexes = input('请输入需要发送的文件编号，多个用英文逗号隔开: ')
        file_index_list = _to_index_list(file_indexes)
        file_paths = [FILE_KEEPER.get_file_path(index)
                      for index in file_index_list]

        body = input('请输入正文内容: ')
        print('已设置')

        to_mails = _split(to_mails)
        cc_mails = _split(cc_mails)
        Utils.send_mail(from_mail, auth_code,
                        to_mails, cc_mails,
                        body, file_paths)
        print('成功发送')

        choice = Utils.choose('是否继续发送邮件(是/否)：', ['是', '否'])
        if choice is None or choice == '否':
            break


def set_path(dir_path):
    """设置工作路径，从指定的路径去找excel文件。"""
    FILE_KEEPER.dir_path = dir_path
