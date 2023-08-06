"""
字符串处理
"""
import json

from ForMark.ForException import exception_return_decorator
from ForMark.ForLog import ForLog


def str_2_file_type(url):
    """根据链接返回图片的类型
    现阶段支持：'pdf', 'video', 'image'
    """
    if url:
        # 将url全部转化成小写
        url = url.lower()
        if url.endswith(('.pdf',)):
            return 'pdf'
        if url.endswith(('.mp4',)):
            return 'video'
        if url.endswith(('.png', '.jpg', '.gif', '.jpeg')):
            return 'image'
    return 'other'


@exception_return_decorator(None)
def str_2_json(s):
    d = json.loads(s)
    return d


def is_none_str(s):
    if isinstance(s, int):
        return False
    if not s or len(str(s.strip())) < 1:
        return True
    return False


def str_to_int(s, default=0):
    if isinstance(s, int):
        return s
    try:
        return int(s)
    except Exception as e:
        ForLog.logger_error(e)
        return default


@exception_return_decorator(0.0)
def str_to_float(s):
    if isinstance(s, float):
        return s
    return float(s)


def str_add_br(s):
    return s
    if '\r\n' in s:
        s = s.replace('\r\n', '<br/>')
    elif '\n' in s:
        s = s.replace('\n', '<br/>')
    return s


if __name__ == '__main__':
    s = """
    (1) 年龄 18-75 岁，性别不限；
(2) 维持性血液透析患者（≥3 个月），每周透析 3 次；
(3) 血红蛋白浓度（Hb）110-130g/L（不含 130g/L）；
(4) 转铁蛋白饱和度(TSAT) 20-50%（不含界值）；
(5) 血清铁血蛋白（SF）200-500μg/L（不含界值）；
(6) 在入组前 12 周内已使用重组人红细胞生成素（EPO）和铁剂治疗；
(7) 自愿签署知情同意书。 
    """
    if ('\r\n' in s):
        s = s.replace('\r\n', '<br/>')
    elif ('\n' in s):
        s = s.replace('\n', '<br/>')
    print('\n' in s)
    print(s)
