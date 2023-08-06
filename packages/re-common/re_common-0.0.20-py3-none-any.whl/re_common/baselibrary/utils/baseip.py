import re
import socket
import time

import requests

from xjlibrary.tools.base_utils import deprecated


@deprecated
def get_ip(proxy=None, count=0):
    """
    获取外网ip
    :return:
    """
    year = str(time.localtime().tm_year)
    url = "http://" + year + ".ip138.com/ic.asp"
    print(url)
    try:
        response = requests.get(url, proxies=proxy, timeout=(30, 60))
        ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response.content.decode(errors='ignore')).group(0)
        return ip
    except Exception as e:
        print(str(e))
        count += 1
        if count > 2:
            print("出现 错误请检查url是否因年份发生改变")
            return False
        return get_ip(proxy, count)


@deprecated
def get_ip2(proxy=None):
    import urllib2
    import re
    url = urllib2.urlopen("http://txt.go.sohu.com/ip/soip", proxies=proxy)
    text = url.read()
    ip = re.findall(r'\d+.\d+.\d+.\d+', text)
    return ip[0]


# 多网卡情况下，根据前缀获取IP
def GetLocalIPByPrefix(prefix):
    """
    prefix = "192.168"
    """
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip
    return localIP


def get_local_ip(ifname='eth0'):
    """
        prefix = enp2s0  or eth0
    :param ifname:
    :return:
    """
    import socket, fcntl, struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])
