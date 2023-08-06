import socket

import click


def net_test(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        click.echo("{}的{}端口连接成功!".format(host, port))
    except socket.error as e:
        click.echo("{}的{}端口连接失败,原因:{}".format(host, port, e))
