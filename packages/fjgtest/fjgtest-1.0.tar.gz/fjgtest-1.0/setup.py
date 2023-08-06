from distutils.core import setup

setup(
    name='fjgtest',  # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试',  #描述
    author='fengjianguo', # 作者
    author_email='395987374@qq.com',
    py_modules=['fjgtest.module_01','fjgtest.module_02'] # 要发布的模块
)
