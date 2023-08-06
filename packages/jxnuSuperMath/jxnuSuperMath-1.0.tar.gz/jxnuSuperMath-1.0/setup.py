from distutils.core import setup

setup(
    name='jxnuSuperMath',    #对外我们模块的名字
    version='1.0',              #版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='wangchao',          #作者
    author_email='2773235996@qq.com',   #作者邮箱
    py_modules=['jxnuSuperMath.demo1','jxnuSuperMath.demo2']  #要发布的模块
)