
from distutils.core import setup
from setuptools import find_packages
setup(
    name = 'mybuilder',     # 包名
    version = '0.0.1',  # 版本号
    description = '上海弥云科技-数据分析模块',
    long_description = '',
    author = 'xinghui.wu',
    author_email = 'xinghui.wu@mii-tec.com',
    url = 'https://github.com/miitec/mybuilder',
    license = '',
    install_requires = [],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities'
    ],
    keywords = '',
    packages = find_packages('src'),  # 必填
    package_dir = {'':'src'},         # 必填
    include_package_data = True,
    )
