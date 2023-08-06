from distutils.core import setup
setup(
    name='dygrlfSuperMath',#对外我们模块的名字
    version='1.0',# 版本号
    description='这是第一个对外发布的模块，测试哦',#描述
    author='lifeng',#作者
    author_email= "dygrlf@126.com",
    py_modules=['01_module','salary'] # 要发布的模块
)