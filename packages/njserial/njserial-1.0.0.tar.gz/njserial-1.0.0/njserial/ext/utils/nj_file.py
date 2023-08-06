import os
import re
import zipfile

from njserial.ext.utils import nj_time

'''
    文件处理模块
    字母存储：ISO-8859-1
'''


def path_exists(path):
    '''
        创建文件夹
    :param path:要创建的文件夹
    :return:
    '''
    if not os.path.exists(path):
        os.makedirs(path)


def get_son_file_info(file_dir, info='files'):
    '''
        获取文件信息
    :param file_dir:当前目录
    :return:
    '''
    for root, dirs, files in os.walk(file_dir):
        if info == 'files':  # 所有非目录子文件
            return files
        if info == 'root':  # 目录路径
            return root
        if info == 'dirs':  # 所有子目录
            return dirs


def mv_file(old_name, new_name):
    '''
        更换文件名
    :param old_name:旧文件名
    :param new_name:新文件名
    :return:
    '''
    os.rename(old_name, new_name)


def judge_file_size(path):
    '''
        判断当前文件大小-如大于50M将文件名称最后位+1
    :param path:文件目录
    :return:修改后文件
    '''
    size = get_doc_size(path)
    if not 'kb' in size:
        if int(re.match(r'\d+', size).group()) < 50 and 'M' in size:
            return path
        else:
            old = re.search(r'{}+(\d+)\.'.format('[\u4e00-\u9fa5]'), path)
            new = re.sub(old.group(1), str(int(old.group(1)) + 1), old.group())
            return re.sub(old.group(), new, path)
    else:
        return path


def add_list(path, list_data, line=True):
    '''
        向文件中写入数据
    :param path:文件目录
    :param list_data:list数据
    :return:成功
    '''
    with open(path, 'a+', encoding="utf-8")as fd:
        count = fd.tell()
        fd.seek(count, 0)
        for i in range(len(list_data)):
            fd.write(list_data[i])
            if line:
                fd.write('\n')
        list_data.clear()  # 插入完清除数据
        fd.close()
        return True


def get_file_name(path):
    '''
        获取地址中文件名称
    :param path:文件地址
    :return:列表[文件名,后缀]
    '''
    if re.search(r'/', path) != None:
        if re.search(r'\.', path) != None:
            a = re.search(r'/(.+)\.(.+)', path)
            return [a.group(1), a.group(2)]
        else:
            return [re.search(r'/(.+)', path).group(1)]
    else:
        if re.search(r'\.', path) != None:
            a = re.search(r'(.+)\.(.+)', path)
            return [a.group(1), a.group(2)]
        else:
            return [path]


def file_add_value(path):
    '''
        向文件第一行中加入数据
    :param path:文件地址
    :return:
    '''
    with open(path, 'a+', encoding="utf-8")as fd:
        count = fd.tell()
        if count == 0:
            fd.write("{} 开始打印数据".format(nj_time.get_time()))
            fd.write('\n')
        fd.close()


def zipDir(dirpath, outFullName):
    """
        压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        fpath = path.replace(dirpath, '')  # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


def get_doc_size(path):
    '''
        获取文件大小
    :param path:文件目录
    :return:文件大小
    '''
    size = os.path.getsize(path)
    return formatSize(size)


def get_file_size(path):
    '''
        获取文件夹大小
    :param path: 文件夹目录
    :return:文件夹大小
    '''
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        print(err)


def read_file(path, keyword, count=0):
    '''
        读取文件
    :param path:文件目录
    :param count:指针指向位置
    :return:包含关键字[]
    '''
    with open(path, 'r', encoding="utf-8")as fd:
        fd.seek(count, 0)  # 指针指向当前count位置
        list1 = []
        while True:
            line = fd.readline()
            if not line:
                fd.close()
                break
            if keyword in line:
                list1.append(line)
        fd.close()
        return list1


def read_file_count(path):
    '''
        读取文件第一行和最后一行
    :param path:文件地址
    :return:第一行和最后一行列表
    '''
    with open(path, 'rb')as fd:
        first_line = fd.readline()  # 取第一行
        offset = -50  # 设置偏移量
        while True:
            fd.seek(offset, 2)  # 指针指向当前offset位置 , whence=2从末尾开始算
            lines = fd.readlines()
            if len(lines) >= 2:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                last_line = lines[-1]  # 取最后一行
                break
            offset *= 2
        fd.close()
        return [first_line.decode(), last_line.decode()]


def formatSize(bytes):
    '''
        字节bytes转化kb\m\g
    :param bytes:
    :return:
    '''
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.0fG" % (G)
        else:
            return "%.0fM" % (M)
    else:
        return "%.0fkb" % (kb)
