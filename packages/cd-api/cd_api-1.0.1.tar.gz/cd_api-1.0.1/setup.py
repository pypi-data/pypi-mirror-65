'''
@说明    :任秋锴的草动api
@时间    :2020/4/2 下午11:11:35
@作者    :任秋锴
@版本    :1.0
'''

from setuptools import setup, find_packages  # 这个包没有的可以pip一下
# import rqk_cd_api

setup(
    name="cd_api",  # 这里是pip项目发布的名称
    version="1.0.1",  # 版本号，数值大的会优先被pip
    keywords=["cdApi", "cd", "rqk"],
    description="任秋锴的草动工具箱",
    long_description="任秋锴的草动工具箱",
    license="MIT Licence",
    url="http://git.renqiukai.com:1983/renqiukai/rqk-cd-tools.git",  # 项目相关文件地址，一般是github
    author="Renqiukai",
    author_email="renqiukai@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests"]  # 这个项目需要的第三方库
)
