import njserial as ser

# python setup.py bdist --format=wininst  生成exe文件
# pyinstaller -F hello.py 生成exe文件
# pip install --pre --upgrade njserial 更新本地环境

# python setup.py sdist 打包成zip文件发布
# twine upload dist/njserial-1.0.0.tar.gz 上传到pypi服务器

if __name__ == "__main__":
    print(ser.print_log('通用固件', 256000, ['COM5']))
