# 版本号  setup.py  ming.py 引用  每次发布 版本+1
import os

version = '1.18'



# 配置目录存放在 用户根目录
default_config_dir = '{}/.ming-tools'.format(os.path.expanduser('~'))
if not os.path.exists(default_config_dir):
    os.makedirs(default_config_dir)
