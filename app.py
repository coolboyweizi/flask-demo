# -*- coding:utf-8 -*-
from flask import Flask, request, g
from libs.imgrizer import Imagrizer
import json
from math import ceil
import time
import urllib
import shutil
from os.path import dirname,exists
from os import sep, makedirs


app = Flask(__name__)
app.secret_key = 'SET_ME_BEFORE_USE_SESSION'


APP_HOST = 'http://app.hsjp138.com/'
APP_ROOT = '/data/www/huishang'


def removeSep(item):
    if item.startswith(sep):
        return removeSep(item[1:])
    else:
        return item

def logger(data):
    if exists('./log') is False :makedirs('./log')
    f = open('./log/'+str(ceil(time.time())),'w')
    f.write(data)
    f.close()

def download(src_img):
    """
    下载原图片。测试用
    :param src_img: 原图片地址
    :return: bool
    """
    src_img = removeSep(src_img)

    if exists(src_img):
        return True

    if exists(dirname(src_img)) is False:
        makedirs(dirname(src_img))

    #url = sep.join((APP_HOST, src_img))
    #urllib.urlretrieve(url, src_img)
    up_file = sep.join((APP_ROOT, src_img))
    shutil.copy(up_file, src_img)

    return exists(src_img)


@app.route('/cutting/', methods=['GET', "POST"])
def cutting():
    """
    http 裁剪入口
    :param:     src 图片原地址
    :param:     md5sun 图片校验码
    :param:     cname 图片裁剪后地址
    :return: json
    """
    if request.method == "POST":
        try:
            md5Sum = request.form.get('md5sum')
            imgFile = removeSep(request.form.get('src'))
            cname = removeSep(request.form.get('dstname'))

            if download(imgFile):
                img = Imagrizer(imgFile, md5Sum)
                img.compress(cname, 200, 200, True)
                #img.compress('200x200/'+cname, 200, 200, True)
                #img.compress('400x400/'+cname, 400, 400, True)
                #img.compress('800x800/'+cname, 800, 800, True)
                return "good"
            else:
                return "bad"

        except IOError as e:
            return str(e)

    else:
        return "GET METHOD"


@app.route('/compress', methods=['POST'])
def compress():
    if request.method != "POST":
        return "bad request"
    try:
        imgFile = removeSep(request.form.get('src'))
        dstname = removeSep(request.form.get('dstname')) # 替换demo
        md5Sum = request.form.get('md5sum')

        if download(imgFile):

            img = Imagrizer(imgFile, md5Sum)

            data = {
                'code': 0,
                'msg': 'compress ok',
            }
            status = False
            for i in (200,400,800):
                dstname = dstname.replace('demo',str(i)+"x"+str(i))
                logger(dstname)
                status = img.compress(dstname, i,i, True)
                if status is False:
                    data = {
                        'code': 10001,
                        'msg': 'compress failure!',
                    }
                    break

    except IOError as e:
        data ={
            'code': -1,
            'msg': str(e)
        }

    logger(json.dumps(data))
    return json.dumps(data)



if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
