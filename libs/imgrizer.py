# -*- coding:utf-8 -*-
'''
图片裁剪

1、裁剪等长宽
2、进行等比例压缩
'''

from os import makedirs
from os.path import exists, splitext, dirname, sep
from PIL import Image
from hashlib import md5


class Imagrizer():
    org_width = 200
    org_height = 200

    def __init__(self, src, md5s):
        """
        图片处理
        :param src: 源文件
        """
        self.src = src
        if exists(src) is False:
            raise IOError("%s not found" % src)

        # MD5文件校正函数
        def md5sum(filename):
            m = md5()
            a_file = open(filename, 'rb')
            m.update(a_file.read())
            a_file.close()
            return m.hexdigest()

        if md5s != md5sum(src):
            raise IOError("%s md5sum not eq" % src)

        # 源图片图片对象
        self.im = Image.open(src)

        # 剪切图片对象
        self.cut = None

        # 压缩图片对象
        self.cpr = None
        self.size = self.im.size

    def _save_img(self, obj, dst):
        """
        存储图片.自动创建目录
        :param obj: 存储对象
        :param dst: 存储位置
        :return: 存储结果
        """
        try:

            if exists(dirname(dst)) is False and dst != "":
                makedirs(dirname(dst))

            obj.save(dst, format='JPEG', quality=90)
        except IOError as e:
            self.error = e.getError()
            return False
        return True

    def cutting(self, dst, dst_w, dst_h):
        """
        图片裁剪
        :param dst:    裁剪存储的文件
        :param dst_w:  裁剪后保留宽
        :param dst_h:  裁剪后保留高
        :return:       bool
        """
        # 分别计算X，Y合理的偏移量
        start_x = int(fabs(self.size[0] - dst_w) / 2)
        start_y = int(fabs(self.size[1] - dst_h) / 2)

        box = (start_x, start_y, start_x + dst_w, start_y + dst_h)
        self.cut = self.im.resize((dst_w, dst_h), Image.ANTIALIAS, box=box)

        return self._save_img(self.cut, dst)

    def compress(self, dst, dst_w, dst_h, cutting=False):
        """
        图片压缩，先进行压缩 后再裁剪
        :param cutting: 是否先进行正规裁剪
        :param dst:  目标地址
        :param dst_w: 裁剪宽度
        :param dst_h: 裁剪高度
        :return:
        """

        if dst_w == 0:
            dst_w = int(self.size[0]/2)
        if dst_h == 0:
            dst_h = int(self.size[1]/2)

        # 是否先裁剪
        if cutting is True:
            w = h = min(self.size[0], self.size[1])
            self.cutting(dst, w, h)
            self.cpr = self.cut.resize((dst_w, dst_h), Image.ANTIALIAS)
        else:
            self.cpr = self.im.resize((dst_w, dst_h), Image.ANTIALIAS)
        return self._save_img(self.cpr, dst)
