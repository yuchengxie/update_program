'''
Description: 
Version: 1.0
Author: xieyucheng
Date: 2021-06-01 09:35:23
LastEditors: xieyucheng
LastEditTime: 2021-06-02 16:27:30
'''
from flask import Flask
import requests
import os
import re
import time
from xml.dom.minidom import parse
import shutil
import zipfile
import subprocess
import psutil as p

XML_FILE_PATH = '/Users/xieyucheng/Desktop/Tmp4/online_update_program/update_program/tmpfile/config/'

SAVE_PROGRAM_DIR = '/Users/xieyucheng/Desktop/Tmp4/online_update_program/update_program/tmpfile/mainprogram/'

MAIN_PRO_ROOT = '/Users/xieyucheng/Desktop/Tmp4/online_update_program/'
MAIN_PRO_PATH = '/Users/xieyucheng/Desktop/Tmp4/online_update_program/main_program/'

XML_URL = 'http://localhost:22088/download/xml/version_main_program.xml'

PRO_URL = 'http://localhost:22088/download/program/main_program.zip'


xmlName = 'version_main_program.xml'
xmlTmpName = 'tmp_version_main_program.xml'

main_pro_name = 'nbc_node_test.py'
main_pro_zip_name = 'main_program.zip'

main_pro_dirname = 'main_program'

program_name = "python3 -u nbc_node_test.py"

app = Flask(__name__)


# @app.route('/')
def compare_version():
    # 比较版本差异-本地版本与线上xml比较
    version_current = readXmlVersion(xmlName)
    # 读取网络上的xml版本,保存为tmp_...xml
    get_file(XML_URL, XML_FILE_PATH, isTmp=True)
    version_net = readXmlVersion(xmlTmpName)
    if version_net > version_current:
        print('有最新版本')
        # 下载主程序
        get_file(PRO_URL, SAVE_PROGRAM_DIR, False)
        # 判断进程是否在 1sha,qi

        # 将旧版本备份
        now = time.time()
        timestamp = '%d' % int(round(now*1000))
        cmd1 = 'cd %s && mv %s %s' % (
            MAIN_PRO_ROOT, main_pro_dirname, main_pro_dirname+'_'+timestamp+'.bak')
        os.popen(cmd1)
        # 将临时文件复制到主程序目录
        shutil.copyfile(os.path.join(SAVE_PROGRAM_DIR, main_pro_zip_name), os.path.join(
            MAIN_PRO_ROOT, main_pro_zip_name))
        time.sleep(0.5)
        # 解压zip
        with zipfile.ZipFile(os.path.join(MAIN_PRO_ROOT, main_pro_zip_name), 'r') as rz:
            rz.extractall(MAIN_PRO_ROOT)
            rz.close()

    else:
        print('没有新版本')


def readXmlVersion(xml_name):
    DomTree = parse(os.path.join(XML_FILE_PATH, xml_name))
    updateList = DomTree.documentElement
    version = updateList.getElementsByTagName('version')
    version = version[0].childNodes[0].data
    return version


def is_alive():
    # 检测是否存活
    cmd = 'ps ef|grep '


def download():
    get_file(XML_URL, XML_FILE_PATH, False)
    get_file(PRO_URL, SAVE_PROGRAM_DIR, False)


def get_file(url, path, isTmp):  # 文件下载函数
    content = requests.get(url)
    # print("write %s in %s" % (url, path))
    filew = ''
    if isTmp:
        filew = open(path+'tmp_'+url.split("/")[-1], 'wb')
    else:
        filew = open(path+url.split("/")[-1], 'wb')
    for chunk in content.iter_content(chunk_size=512 * 1024):
        if chunk:  # filter out keep-alive new chunks
            filew.write(chunk)
    filew.close()


def get_process_id():
    # child = subprocess.Popen(["pgrep", "-f", program_name], stdout=subprocess.PIPE, shell=False)
    child = subprocess.Popen(
        ["ps -ef|grep %s" % program_name], stdout=subprocess.PIPE, shell=False)
    print(child)
    # child = subprocess.Popen(
    #     ["ps -ef|grep %s" % program_name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    print(response)
    response = str(response, encoding='utf-8')
    response = response.split('\n')
    while '' in response:
        response.remove('')
    return response


def get_pid(name):
    # pid1 = os.popen( 'ps -ef | grep python3 -u nbc_node_test.py')
    pid1 = os.popen("ps -ef | grep nbc_node_test.py")
    pid1 = pid1.read()
    print('pid1:', pid1)
    # pid2 = pid1.read()[11:14]
    # print('pid2:',pid2)
    pass
    # process_list = psutil
    # regex = "pid=(\d+),\sname=\'" + name + "\'"
    # print(regex)
    # pid = 0
    # for line in process_list:
    #     process_info = str(line)
    #     ini_regex = re.compile(regex)
    #     result = ini_regex.search(process_info)
    #     if result != None:
    #         # pid = string.atoi(result.group(1))
    #         print(result.group())
    #         break
# if __name__ == '__main__':
#     print('update_program')
#     app.run(host='0.0.0.0', port=5000)


# download() dd

id = get_process_id()
print(id)
# compare_version()
# get_pid(program_name)
