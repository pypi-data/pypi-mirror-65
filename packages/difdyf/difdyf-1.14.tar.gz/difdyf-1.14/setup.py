from setuptools import setup

setup(
    name='difdyf',# 需要打包的名字,即本模块要发布的名字
    version='v1.14',#版本
    description='A  module for diff geo', # 简要描述
    py_modules=[],   #  需要打包的模块
    packages=['','difdyf'],
    package_dir={'difdyf':'difdyf'},
    author='dyf', # 作者名
    author_email='715017912@qq.com',   # 作者邮件
    url='https://github.com/yftheone1995/dyf@riec.tohoku.ac.jp', # 项目地址,一般是代码托管的网站
    requires=['numpy','sympy'], # 依赖包,如果没有,可以不要
    license='MIT'
)