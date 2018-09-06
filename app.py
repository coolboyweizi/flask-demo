# -*- coding:utf-8 -*-
from flask import Flask, request, g
from libs.imgrizer import Imagrizer
import json

app = Flask(__name__)
app.secret_key = 'SET_ME_BEFORE_USE_SESSION'



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
            imgFile = request.form.get('src')
            md5Sum = request.form.get('md5sum')
            cname = request.form.get('cname')
            img = Imagrizer(imgFile, md5Sum)
            img.compress(cname, 200, 200, True)
            return "aaaa"
        except IOError as e:
            return str(e)
        return "sss"
    else:
        return "GET METHOD"


@app.route('/compress', methods=['POST'])
def compress():
    if request.method != "POST":
        return "bad request"

    try:
        imgFile = request.form.get('src')
        md5Sum = request.form.get('md5sum')
        dstname = request.form.get('cname')
        img = Imagrizer(imgFile, md5Sum)

        if img.compress(dstname, 200, 200, True):
            return json.dumps({
                'code': 0,
                'msg': 'compress success !',
                'path': dstname
            })
        else:
            return json.dumps({
                'code': 10001,
                'msg': 'compress failure!',
            })

    except IOError as e:
        return json.dumps({
            'code': -1,
            'msg': str(e)
        })


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
