# -*- coding: utf-8 -*-
import os
bmw_dir = os.path.dirname(os.path.dirname(__file__))  # 拿到bmw路径名称
images_path = os.path.join(bmw_dir,"images")
# print(images_path)
# 判断images文件夹是否存在
if not os.path.exists(images_path):
    # print("images文件夹不存在")
    os.mkdir(images_path)
else:
    print("存在")
