
from flash_handler.log import logger


class Error(object):
    """
    TODO: 当前尚未梳理错误类型。待完成梳理，请修改代码以提供更明确的错误信息。
    """
    @staticmethod
    def empty_input():
        logger.error('抱歉，你的输入有误，操作中止')

    @staticmethod
    def illegal_input():
        logger.error('抱歉，没有这个选项，请重新选择')

    @staticmethod
    def empty_query_result():
        logger.error('查询结果的格式错误')
