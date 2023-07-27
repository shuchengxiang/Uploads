# -*- coding: utf-8 -*-
import os
import shutil
import json

from flask import Blueprint, request, send_file, jsonify
from utils import load_json_data, load_txt_data, load_yaml_data, write_json_data, write_txt_data, write_yaml_data

api = Blueprint('api', __name__, template_folder='templates')

default_upload_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
upload_path = os.getenv('upload_path', default_upload_path)


def response_data(data, code=0, message=''):
    return_data = {
        'code': 0,
        'message': '',
        'data': None,
    }
    return_data['data'] = data
    return_data['code'] = code
    return_data['message'] = message
    return json.dumps(return_data, indent=4, ensure_ascii=False)

@api.route('/data-manage/files/', methods=['GET'])
@api.route('/data-manage/files/<path:path>', methods=['GET'])
def get_files(path=''):
    file_list = []
    file_path = os.path.join(upload_path, path)
    if os.path.isdir(file_path):
        file_list = os.listdir(file_path)

    return response_data(file_list)

@api.route('/data-manage/files', methods=['POST'])
def upload_file():
    file_path = request.form.get('file_path') or ''
    
    for file in request.files.getlist('files'):
        try:
            savename = file.save(os.path.join(upload_path, file_path, file.filename))
        except Exception as e:
            print(e)

    return response_data('success')

@api.route('/data-manage/files/read/<path:path>', methods=['GET'])
def read_file(path):
    file_type = request.form.get('file_type')
    file_path = os.path.join(upload_path, path)
    if os.path.isfile(file_path):
        content = ''
        if file_type == 'json':
            content = load_json_data(file_path)
        elif file_type == 'yaml':
            content = load_yaml_data(file_path)
        elif file_type == 'txt':
            content = load_txt_data(file_path)
        else:
            file_path = file_path.replace('\\', '/')
            return send_file(file_path)

        return response_data(content)
    else:
        return response_data(None, -1, '无此文件')

@api.route('/data-manage/files/write/<path:path>', methods=['POST'])
def write_file(path):
    file_type = request.json.get('file_type')
    is_force = request.json.get('force')
    content = request.json.get('content')
    file_path = os.path.join(upload_path, path)
    if not is_force and os.path.isfile(file_path):
        return response_data(None, 0, '文件已存在')

    if file_type == 'json':
        write_json_data(file_path, content)
    elif file_type == 'yaml':
        write_yaml_data(file_path, content)
    elif file_type == 'txt':
        write_txt_data(file_path, content)
    else:
        return response_data(None, -1, '不支持的文件格式')

    return response_data(None, 0, '成功')

@api.route('/data-manage/files/<path:path>', methods=['DELETE'])
def delete_file(path):
    file_path = os.path.join(upload_path, path)
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        os.remove(file_path)
    return response_data('success')
