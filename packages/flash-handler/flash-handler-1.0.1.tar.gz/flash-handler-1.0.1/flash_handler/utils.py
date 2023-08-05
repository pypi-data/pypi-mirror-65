
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import smtplib

from flash_handler.config import Config
from flash_handler.const import Const
from flash_handler.error import Error


class Utils(object):
    @staticmethod
    def to_chart_type(type_repr):
        """把图表种类对外展现的名称转化为内部表示。转化失败时返回None。"""
        if type_repr not in Const.CHART_REPR2TYPE:
            return None
        return Const.CHART_REPR2TYPE[type_repr]

    @staticmethod
    def to_method_type(type_repr):
        """把图表纵坐标（柱状图或折线图）或统计量（饼图）计算方法对外展现的名称转化为内部表示。
        转化失败时返回None。"""
        if type_repr not in Const.METHOD_REPR2TYPE:
            return None
        return Const.METHOD_REPR2TYPE[type_repr]

    @staticmethod
    def get_all_methods(delimeter='/'):
        """把程序所支持的、图表纵坐标（柱状图或折线图）或统计量（饼图）的所有计算方法对外展现的
        名称（计数或加和）用分隔符连接起来，得到字符串供调用者进行打印。"""
        return delimeter.join([Const.METHOD_SUM_REPR, Const.METHOD_COUNT_REPR])

    @staticmethod
    def print_table_df(file_index, file_name, df):
        """打印数据df。数据df的来源文件的索引是file_index，文件名是file_name。"""
        print('表{}, {}'.format(file_index, file_name))
        print('-' * 60)
        print(df.to_string(index=False))
        print('')

    @staticmethod
    def send_mail(from_mail, auth_code,
                  to_mails, cc_mails,
                  body, file_paths=None):
        """以from_mail为发送人邮箱、auth_code为发送邮件所需要的授权码、
        to_mails为目标邮箱列表、cc_mails为抄送人邮箱列表、body为邮件正文、
        file_paths为邮件附件，发送邮件。file_paths默认为`None`，表示邮件不带附件。"""
        smtp = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT)

        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_mail, auth_code)

        msg = MIMEMultipart()
        msg['Subject'] = Config.SMTP_MAIL_SUBJECT
        msg['From'] = from_mail
        msg['To'] = ','.join(to_mails)
        msg['Cc'] = ','.join(cc_mails)

        # 正文内容换行
        if file_paths:
            body += '\n'
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            for file_path in file_paths:
                file_name = os.path.basename(file_path)
                with open(file_path, "rb") as f:
                    attachment = MIMEApplication(f.read())
                    attachment['Content-Type'] = 'application/octet-stream'
                    attachment.add_header('Content-Disposition',
                                          'attachment',
                                          filename=file_name)
                    msg.attach(attachment)

        smtp.sendmail(from_mail, cc_mails + to_mails, msg.as_string())

    @staticmethod
    def is_empty(s):
        """注意：该函数先去掉首尾空格再判断是否为空"""
        return 0 == len(s.strip())

    @staticmethod
    def choose(prompt, choices):
        """若输入为空，要终止操作（需要调用者配合）；若输入了“非选项内容”，要继续输入。"""
        while True:
            choice = input(prompt)

            if Utils.is_empty(choice):
                Error.empty_input()
                return None

            if choice in choices:
                return choice

            Error.illegal_input()
