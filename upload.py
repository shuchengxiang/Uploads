# -*- coding: utf-8 -*-
import os
import zipfile
import shutil

from flask import Flask, render_template, redirect, request, send_file
from flask_uploads import UploadSet, configure_uploads, patch_request_class, \
      DEFAULTS, ARCHIVES, AUDIO, EXECUTABLES, SCRIPTS
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


app = Flask(__name__,template_folder='./templates')

upload_path = os.path.join(os.path.dirname(__file__),'uploads')
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_FILES_DEST'] = upload_path
app.config['UPLOADED_FILES_'] = upload_path
app.config['UPLOADED_DEFAULT_DEST'] =upload_path
app.config['UPLOADED_DEFAULT_URL'] = upload_path
# app.config['UPLOADED_X_DENY'] = []

# OTHER = tuple('css html ico woff2 cur log image/jpeg'.split())
files = UploadSet('files', DEFAULTS+AUDIO+ARCHIVES+SCRIPTS+EXECUTABLES)
configure_uploads(app, files)
patch_request_class(app, size=15 * 1024 * 1024 * 1024)  # set maximum file size, default is 64MB


class UploadForm(FlaskForm):
    files = FileField(validators=[FileAllowed(files, u'不支持该文件类型'), FileRequired(u'请选择文件上传!')])
    submit = SubmitField(u'上传')


def getAllDirRE(path, sp=""):
    # 得到当前目录下所有的文件
    filesList = os.listdir(path)
    if not filesList:
        return
    # 处理每一个文件
    sp += "   "
    for fileName in filesList:
        try:
            filename = fileName.encode('cp437').decode('utf-8')
        except:
            filename = fileName.encode('utf-8').decode('utf-8')
        os.chdir(path)
        os.rename(fileName, filename)  # 重命名文件
        # 判断是否是路径（用绝对路径）
        fileAbsPath = os.path.join(path, filename)
        if os.path.isdir(fileAbsPath):
            # print(sp + "目录：", fileName)
            # 递归调用
            getAllDirRE(fileAbsPath, sp)
        else:
            # print(sp + "普通文件：", fileName)
            pass


def unzip_file(zip_src, dst_dir):
    """
    解压zip文件
    :param zip_src: zip文件的全路径
    :param dst_dir: 要解压到的目的文件夹
    :return:
    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        fz.close()
        getAllDirRE(dst_dir)
        # 解压并重命名之后，需切换目录，
        os.chdir(app.config['UPLOADED_FILES_DEST'])
    else:
        return "请上传zip类型压缩文件"


@app.route('/scx_upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('files'):
            # name = hashlib.md5(('admin' + str(time.time())).encode('utf-8')).hexdigest()[:15]
            name = filename.filename
        # try:
            savename = files.save(filename, name=name)
            if zipfile.is_zipfile(app.config['UPLOADED_FILES_DEST'] + "\\" + name):
                unzip_file(app.config['UPLOADED_FILES_DEST'] + "\\" + name,
                           app.config['UPLOADED_FILES_DEST'] + "\\" + savename.split('.')[0])
        # except:
        #     print(filename)
        success = True
    else:
        success = False
    return render_template('file_index.html', form=form, success=success)


@app.route('/manage')
def manage_file():
    files_list = os.listdir(app.config['UPLOADED_FILES_DEST'])
    file_path = files.path('.')
    for i in range(len(files_list)):
        if os.path.isdir(os.path.join(file_path,files_list[i])):
            files_list[i] = files_list[i] + '/'
    return render_template('file_manage.html', files_list=files_list, path='')


@app.route('/open/<path:path>')
def open_file(path):
    file_path = files.path(path)
    if os.path.isdir(file_path):
        files_list = os.listdir(file_path)
        for i in range(len(files_list)):
            if os.path.isdir(os.path.join(file_path,files_list[i])):
                files_list[i] = files_list[i] + '/'
        # if path[-1] == '/':
        #     pass
        # else:
        #     path = path+'/'
        return render_template('file_manage.html', files_list=files_list, path=path)
    else:
        file_path = file_path.replace('\\', '/')
        return send_file(file_path)


@app.route('/delete/<path:path>')
def delete_file(path):
    file_path = files.path(path)
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        os.remove(file_path)
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(debug=True)