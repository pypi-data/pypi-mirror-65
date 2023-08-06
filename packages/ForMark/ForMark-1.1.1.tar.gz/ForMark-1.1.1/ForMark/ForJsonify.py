from flask import jsonify as jsonify_deity

Error_Code = {
    10001: "缺少必填参数",
    10002: "参数类型错误",
    10003: "可选参数错误",
    10004: "信息上传重复",  # 例如相同手机号已经注册了账户
    10005: "无指定数据",  # 例如根据id寻找指定信息时，无指定信息
    10006: "上传数据不合理",  # 例如商品价格<=0
    10007: "无指定接口",
    10008: "无权限",
    10009: "失败",
}


def jsonify_success(data=None, msg=None):
    return jsonify(True, 0, msg, data)


def jsonify_fail(code=0, msg=None):
    return jsonify(False, code, msg)


def jsonify(success=False, code=0, msg=None, data=None):
    if not msg:
        if success:
            msg = "成功"
        else:
            msg = Error_Code[code]
    return jsonify_deity(success=success, code=code, msg=msg, data=data)
