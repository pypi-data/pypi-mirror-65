from setuptools import setup

setup(
    name="njserial",  # 这里是pip项目发布的名称
    version="1.0.1",  # 版本号，数值大的会优先被pip
    keywords=("pip", "SICA", "featureextraction"),
    description="Serial Tool",  # 平台提示
    long_description="Automated Packaging Tool",
    license="MIT Licence",

    url="https://github.com/congrenya/njtest/blob/master/njtest.py",  # 项目相关文件地址，一般是github
    author="Stephen Yao",
    author_email="a1123547734@163.com",

    packages=['njserial', 'njserial.cli', 'njserial.ext', 'njserial.ext.utils'],
    # 打包文件夹
    include_package_data=True,  # 自动打包文件夹内所有数据
    zip_safe=True,  # 设定项目包为安全，不用每次都检测其安全性
    platforms="any",
    install_requires=['pyserial', 'openpyxl']  # 这个项目需要的第三方库
)
