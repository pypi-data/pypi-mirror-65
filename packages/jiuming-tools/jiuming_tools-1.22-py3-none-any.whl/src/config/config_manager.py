import os
import time

import click
import yaml
from git import Repo

from src.config.global_config import default_config_dir

# 默认配置file
sync_config_default_file = default_config_dir + '/sync_config.yaml'
# 配置默认目录 建立git 仓库
repo = Repo.init(default_config_dir)


def details():
    checkSyncConfig()
    y_read_file = open(sync_config_default_file, 'r')
    config = yaml.safe_load(y_read_file)
    if config is None:
        click.echo("暂无同步仓库配置信息!")
        return
    else:
        sc = SyncConfig.to_obj(config[0])
        click.echo("仓库地址:{},用户名:{},密码:{}".format(sc.url, sc.username, sc.password))


def save(url, username, password):
    """
    创建配置  多次创建 会依次覆盖
    :param url:  同步仓库url
    :param username:  同步仓库用户名
    :param password:  同步仓库密码
    :return:
    """
    y_file = open(sync_config_default_file, 'w')
    sc = SyncConfig(url=url, username=username, password=password)
    yaml.safe_dump([sc.__dict__], y_file)
    repo.create_remote("origin", url)
    click.echo('\n录入的同步仓库信息:\n地址:{},用户名:{},密码:{}'.format(url, username, password))


def remove():
    """
    删除 配置文件
    :return:
    """
    try:
        checkSyncConfig()
        os.unlink(sync_config_default_file)
        repo.delete_remote("origin")
    except OSError:
        click.echo("删除同步仓库配置失败")
    else:
        click.echo("删除同步仓库配置")


def pull():
    checkSyncConfig()
    repo.remote().pull()
    click.echo("sync pull config")


def push():
    checkSyncConfig()
    git = repo.git
    git.add('./*')
    # 当工作区不是干净的 就进行 commit -》 push
    commit_str = '\'{},同步jiuming-tools配置\''.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    git.commit('-m {}'.format(commit_str))
    git.push()
    click.echo("推送配置：{}".format(commit_str))


def checkSyncConfig():
    """
    检查 配置文件是否存在
    :return:
    """
    if not os.path.exists(sync_config_default_file):
        raise Exception(click.echo("同步仓库配置不存在,请创建同步配置"))


class SyncConfig(object):
    """
    同步配置 对象
    暂时只支持 http/https 协议git 操作
    """
    # 地址
    url: str
    # git用户名
    username: str
    # 密码
    password: str

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    @staticmethod
    def to_obj(d: dict):
        """
        将读取的dict 转换为 serverConfig
        :param d:  dict
        :return: ServerConfig
        """
        return SyncConfig(url=d['url'], username=d['username'],
                          password=d['password'])
