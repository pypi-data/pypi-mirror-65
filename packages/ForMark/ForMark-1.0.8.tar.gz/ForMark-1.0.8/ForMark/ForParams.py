from functools import wraps

from flask import g, jsonify


def get_params(params=None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if params:
                if not g.params:
                    return jsonify(success=False, msg='缺少必填参数', code='10001')
                for item in params.items():
                    key = g.params.get(item[0], None)
                    print("参数",key)
                    if key is None:
                        return jsonify(success=False, msg=item[1], code='10001')
                    g.setdefault(item[0], key)
            return func(*args, **kwargs)
        return inner
    return wrapper
