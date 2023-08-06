import threading
import time
from serial import Serial
from njserial.ext.utils import nj_parse, nj_time, nj_file
from njserial.utils import check_alive
import serial.tools.list_ports

'''
    串口通讯模块
'''


class NjSerial(Serial):
    #     '''
    #         连接串口
    #     :param port:端口号
    #     :param baudrate:波特率(普通模块:9600,115200，5981:256000)
    #     :param bytesize:数据位
    #     :param parity:效验位('N', 'E', 'O', 'M', 'S')
    #     :param stopbits:停止位
    #     '''

    @check_alive
    def start_log(self):
        self.state = True
        self.thread_read = threading.Thread(target=self.start_read_cmd, args=())
        self.thread_read.start()
        if self.baudrate == 9600:
            self.thread_read_9600 = threading.Thread(target=self.start_9600, args=())
            self.thread_read_9600.start()

    @check_alive
    def start_read_cmd(self):
        '''
            开启读取串口数据
        :return:
        '''
        self.tips = 1
        self.serial_data = []
        self.serial_data_115200list = []
        while self.state:
            try:
                if self.isOpen():
                    if self.baudrate != 9600:
                        data = self.readline()
                        if data != b'':
                            content = nj_parse.bytes_to_str(data, encoding="utf-8")
                            datas = content.replace('\n', '').replace('\r', '')  # 去除换行
                            self.serial_data_115200list.append(add_time(datas))  # 添加115200打印数据
                    else:
                        data = self.read()
                        self.serial_data.append(data)
                        self.start_time = time.time()
                        # print(nj_parse.bytes_to_hexstr(data)) # 查看9600单个数据
                    if self.tips > 0:
                        self.tips -= 1
                        print("{} ：{}".format(self.port, add_time(data)))  # 刚启动时打印数据
            except Exception as err:
                print("读取串口数据报错" + str(err))

    @check_alive
    def start_9600(self):
        '''
            9600循环数据打印
        @return:
        '''
        self.serial_data_9600list = []
        while self.state:
            if (time.time() - self.start_time) >= 0.06 and len(self.serial_data) > 4:
                self.content = nj_parse.list_bytes_to_hexstr(self.serial_data)
                self.serial_data = []
                self.start_time = time.time()
                self.serial_data_9600list.append(add_time(self.content))
                # print("结果：" + self.add_time(self.content))

    @check_alive
    def stop_serial(self):
        '''
            关闭串口连接
        :return:
        '''
        self.state = False
        time.sleep(0.5)
        self.close()


def add_time(data, value=''):
    '''
        为数据增加时间节点
    :param data:初始数据
    :param value:中间要插入的数据
    :return:合并后数据
    '''
    return "{} {}{}".format(nj_time.get_time(), value, data)


def print_log(path, baudrate, cmd_list):
    '''
        打印串口日志
    @param path:目录文件夹名
    @param baudrate:波特率
    @param cmd_list:串口端口
    @return:
    '''
    nj_file.path_exists(path)  # 判断文件夹
    print(get_port())  # 打印当前所有端口
    if len(cmd_list) > 0:
        for cmd in cmd_list:
            threading.Thread(target=keep_data, args=(path, cmd, baudrate, False)).start()
    else:
        time.sleep(1)
        port_list = check_port()  # 检查可用端口
        if not len(port_list) > 0:
            raise NameError('目前无串口可用,请插入新串口')
        for cmd in port_list:
            threading.Thread(target=keep_data, args=(path, cmd, baudrate, True)).start()
        time.sleep(5)
        print("{}-->新增串口：{}".format(path, str(PORT)))


PORT = []


def keep_data(path, cmd, baudrate=115200, prints=False):
    global PORT
    '''
        保存打印数据
    :param path: 文件保存目录
    :param cmd:端口号
    :param prints:判断是否打印正连接的端口号
    :return:
    '''
    file_path = "{}/{}日志1.log".format(path, cmd)
    try:
        ser = NjSerial(cmd, baudrate)
        ser.start_log()
        while True:
            nj_file.file_add_value(file_path)  # 增加开始打印时间
            time.sleep(4)
            if len(ser.serial_data_115200list) > 0:
                if prints:  # 判断初始为空端口
                    PORT.append(cmd)
                nj_file.add_list(file_path, ser.serial_data_115200list)  # 保存数据
                file_path = nj_file.judge_file_size(file_path)  # 判断文件大小
            time.sleep(27)
    except Exception as err:
        print("串口日志报错：" + str(err))


def check_port():
    '''
        打印可用端口
    :return:返回可用端口列表
    '''
    serial_list = []
    for i in get_port():
        try:
            ser = NjSerial(port=i)
            ser.close()
            serial_list.append(i)
        except Exception as err:
            pass
    return serial_list


def get_port():
    '''
        获取所有串口号
    :return: 所有串口的名字-->如‘com3’
    '''
    all_serial_list = show_all_serial()
    usb_serial_list = []
    for i in all_serial_list:
        if 'USB Serial Port' in i[1]:
            usb_serial_list.append(i[0])
    return usb_serial_list


def show_all_serial():
    '''
        获取所有的串口信息
    :return:所有的串口及每个窜口的信息
    '''
    plist = list(serial.tools.list_ports.comports())  # 获取串口信息
    all_serial_list = []
    for p in plist:
        serial_info = []
        for i in p:
            serial_info.append(i)
        all_serial_list.append(tuple(serial_info))
    return all_serial_list
