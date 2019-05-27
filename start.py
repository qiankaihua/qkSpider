# coding=utf-8
import os
import json
# reload(sys)
# sys.setdefaultencoding('utf-8')

from flask import Flask
from flask import request
import flask_restful


app = Flask(__name__)
api = flask_restful.Api(app)

def clean_file(filename):
    f = open(filename, 'w')
    f.truncate()
    return

def start_spider(data):
    data_str = json.dumps(data)
    # print(data_str)
    # print('scrapy crawl zhihu -a arg=\'' + data_str + '\' -o ms.json')
    os.popen('scrapy crawl zhihu -a arg=\'' + data_str + '\' -o ms.json').read()
    return

def read_result(filename):
    file = open(filename, 'r')
    json_str = json.load(file)
    file.close()
    return json_str

class HelloWorld(flask_restful.Resource):
    def post(self):
        data = request.json
        class_dict = data.get('classList', [])
        _id = data.get('id', '')
        url = data.get('url', '')
        nxt_url = data.get('nextUrl', '')
        child_class_list = data.get('childPosition', [])
        # print(class_dict)
        # print(_id)
        # print(url)
        # print(nxt_url)
        # print(child_class_list)
        data_dict = {
            'el_class': class_dict,
            'el_id': _id,
            'url': url,
            'nxt_url': nxt_url,
            'child_class_list': child_class_list,
        }
        clean_file('./ms.json')
        start_spider(data_dict)
        json_str = read_result('./ms.json')
        return json_str

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='localhost')