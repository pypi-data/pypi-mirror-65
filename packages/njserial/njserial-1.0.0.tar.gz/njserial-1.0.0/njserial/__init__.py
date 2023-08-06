from njserial.ext import nj_serial, count


def print_log(path, baudrate, cmd_list):
    '''
        打印串口日志
    @param path:目录文件夹名
    @param cmd_list:串口端口
    @param baudrate:打印波特率
    @return:
    '''
    nj_serial.print_log(path, baudrate, cmd_list)


def conut_reconnect_data(excel_path, excel_sheet, path, key):
    '''
        分析重连异常日志
    @param excel_path:断电excel文件路径
    @param excel_sheet:excel表名称
    @param path:日志目录名
    @param key:在线关键字--> network status:9
    @return:
    '''
    count.analysis(excel_path, excel_sheet, path, key)


def conut_on_data(path, key1, key2, new_path):
    '''
        分析在线日志
    @param path:日志目录路径
    @param key1:在线关键字
    @param key2:离线关键字
    @param new_path:新的文件-->'./test.xlsx'
    @return:
    '''
    count.on_line(path, key1, key2, new_path)


if __name__ == '__main__':
    print_log('通用固件', 256000, ['COM5'])
    print_log('通用固件1', 115200, [])
