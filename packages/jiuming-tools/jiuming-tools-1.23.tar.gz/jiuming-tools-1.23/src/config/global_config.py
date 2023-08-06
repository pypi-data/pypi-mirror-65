import os
import re

# 版本号  setup.py  ming.py 引用  每次发布 版本+1
version = '1.23'

# 配置目录存放在 用户根目录
default_config_dir = '{}/.ming-tools'.format(os.path.expanduser('~'))
if not os.path.exists(default_config_dir):
    os.makedirs(default_config_dir)

# 正则
compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
compile_host_mame = re.compile('^[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?$')
