# coding=utf-8
"""参数含义：
version：值为1~40的整数，控制二维码的大小（最小值是1，是个12×12的矩阵）。 如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。

error_correction：控制二维码的错误纠正功能。可取值下列4个常量。
　　ERROR_CORRECT_L：大约7%或更少的错误能被纠正。
　　ERROR_CORRECT_M（默认）：大约15%或更少的错误能被纠正。
　　ROR_CORRECT_H：大约30%或更少的错误能被纠正。

box_size：控制二维码中每个小格子包含的像素数。

border：控制边框（二维码与图片边界的距离）包含的格子数（默认为4，是相关标准规定的最小值）

"""
from ForMark import ForFile

'''
【红色】：red 【橙色】：orange 【黄色】：yellow 【绿】：green 【 蓝】：blue【紫】：purple 
【灰色】：gray 【白色】：white 【粉红色】：pink 【黑色】：black【墨绿色】：dark green 【橙红色】：orange-red
'''
import uuid
import os


def getQRcodeNoImg(strs, old=False,authority=0):
    """
    参数含义：
        version：值为1~40的整数，控制二维码的大小（最小值是1，是个12×12的矩阵）。
         如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
        
        error_correction：控制二维码的错误纠正功能。可取值下列4个常量。
　　              ERROR_CORRECT_L：大约7%或更少的错误能被纠正。
　　              ERROR_CORRECT_M（默认）：大约15%或更少的错误能被纠正。
　　              ROR_CORRECT_H：大约30%或更少的错误能被纠正。

        box_size：控制二维码中每个小格子包含的像素数。

        border：控制边框（二维码与图片边界的距离）包含的格子数（默认为4，是相关标准规定的最小值）
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=50,
        border=0,
    )
    # 添加数据
    qr.add_data(strs)
    # 填充数据
    qr.make(fit=True)
    # 生成图片
    if old:
        img = qr.make_image(fill_color="#cccccc", back_color="white")
        img = img.convert("RGBA")  # RGBA\CMYK

    else:
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.convert("RGBA")  # RGBA\CMYK
    # 目录不存在,则自动创建目录
    folder = current_app.root_path + '/tmp/'
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_name = str(uuid.uuid1()) + ".png"
    local_url = folder + file_name
    # print("文件",local_url)
    img.save(local_url)
    status, key = ForFile.get_url_from_file(file_name, local_url)
    if status == 200:
        # 获取加密后的文件key后，保存到数据库
        annex = Annex()
        annex.name =file_name
        annex.title = "二维码"
        annex.introduce =  "二维码"
        annex.key = key
        annex.authority = authority
        annex.to_new_save()
        return annex.url
    return ''


