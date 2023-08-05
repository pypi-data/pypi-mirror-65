
class Const(object):
    DELIMETERS = ',|，'
    """合法分隔符。可用于分割用户输入的字符串。"""

    # 以下type的取值必须是matplotlib支持的图表类型（plot方法的kind参数允许的值）
    CHART_BAR_TYPE = 'bar'
    CHART_PIE_TYPE = 'pie'
    CHART_LINE_TYPE = 'line'
    """图表类型的内部表示"""

    CHART_BAR_REPR = '柱状图'
    CHART_PIE_REPR = '饼图'
    CHART_LINE_REPR = '折线图'
    """图表类型对外展现的名称"""

    CHART_REPR2TYPE = {
        CHART_BAR_REPR: CHART_BAR_TYPE,
        CHART_PIE_REPR: CHART_PIE_TYPE,
        CHART_LINE_REPR: CHART_LINE_TYPE,
    }
    """图表种类对外展现的名称和内部表示的映射关系"""

    METHOD_SUM_TYPE = 'sum'
    METHOD_COUNT_TYPE = 'count'
    """图表纵坐标（柱状图或折线图）或统计量（饼图）计算方法的内部表示"""

    METHOD_SUM_REPR = '加和'
    METHOD_COUNT_REPR = '计数'
    """图表纵坐标（柱状图或折线图）或统计量（饼图）计算方法对外展现的名称"""

    METHOD_REPR2TYPE = {
        METHOD_SUM_REPR: METHOD_SUM_TYPE,
        METHOD_COUNT_REPR: METHOD_COUNT_TYPE,
    }
    """图表纵坐标（柱状图或折线图）或统计量（饼图）计算方法对外展现的名称和内部表示之间的映射
    关系"""
