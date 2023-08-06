"""
异常处理
"""
from ForMark.ForLog import ForLog


def exception_return_decorator(result):
    """
    异常收集，并返回指定数据
    :param result:
    :return:
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ForLog.show(func, e)
                return result

        return inner

    return wrapper


@exception_return_decorator(result=1)
def mark(name):
    1 / 0
    print(123, name)
    return 333


if __name__ == '__main__':
    print(mark('444'))
