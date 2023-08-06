def check_alive(fn):
    '''
        检查串口是否开启
    @param fn:
    @return:
    '''

    def inner(self, *args, **kwargs):
        if not self.isOpen():  # 判断串口是否连接
            raise NameError('串口未连接,请重试')
        return fn(self, *args, **kwargs)

    return inner
