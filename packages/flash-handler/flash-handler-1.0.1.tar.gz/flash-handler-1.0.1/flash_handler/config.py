import os


class Config(object):
    DIR_PATH = os.getenv('FBD_DIR_PATH', 'static')
    """工作目录。程序将从此处获取Excel文件。"""

    SMTP_HOST = 'smtp.qq.com'
    """邮件服务器主机名"""
    SMTP_PORT = 587
    """邮件服务器端口"""
    SMTP_MAIL_SUBJECT = 'python发送附件'
    """邮件主题"""
