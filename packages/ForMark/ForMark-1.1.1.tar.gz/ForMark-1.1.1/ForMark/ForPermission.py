from functools import wraps

from flask import session, g

from ForMark.ForJsonify import jsonify_fail


def permission_check(authority, category=None):
    """
    category:为了进一步控制权限而加入
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user_id = session.get('user_id', None)
            # print("用户id", user_id)
            # if not user_id:
            #     if authority == NO_LOGIN:
            #         g.user = None
            #         return func(*args, **kwargs)
            #     return jsonify_fail(code=10008)
            # user = User.objects(id=user_id).first()
            # if not user:
            #     return jsonify_fail(code=10008)
            # if authority < user.authority:
            #     return jsonify_fail(code=10008)
            # g.user = user
            return func(*args, **kwargs)

        return inner

    return wrapper


@permission_check(33)
def mark():
    print(1)


if __name__ == '__main__':
    mark()
    pass
