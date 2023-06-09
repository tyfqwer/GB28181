import socket, random
from threading import Thread
import time

# 定义源IP地址和端口
src_ip = '192.168.1.120'
src_port = 15060

host = '192.168.1.120'  # 服务端ip
port = 5060  # 服务端ip端口

n = 0


# --------------------------注意必须\r\n结尾，否则m7s解析不出来
def register(s):
    global n
    str_send = 'REGISTER sip:34020000002000000001@3402000000 SIP/2.0\r\n'
    str_send += 'Via: SIP/2.0/UDP {}:{};rport;branch=z9hG4bK536519180\r\n'.format(src_ip, src_port)
    str_send += 'From: <sip:34020000001320000001@3402000000>;tag=1895943811\r\n'
    str_send += 'To: <sip:34020000001320000001@3402000000>\r\n'
    str_send += 'Call-ID: 1821358258\r\n'
    str_send += 'CSeq: 1 REGISTER\r\n'
    str_send += 'Contact: <sip:34020000001320000001@{}:{}>\r\n'.format(src_ip, src_port)
    str_send += 'Max-Forwards: 70\r\n'
    str_send += 'User-Agent: IP Camera\r\n'
    str_send += 'Expires: 3600\r\n'
    str_send += 'Content-Length: 0\r\n\r\n'
    print(str_send)
    b4 = str_send.encode()
    s.sendto(b4, (host, port))


def message(s):
    str_send = 'MESSAGE sip:34020000001320000001@3402000000 SIP/2.0\n'
    str_send += 'Via: SIP/2.0/UDP 192.168.1.120:5060;branch=z9hG4bK.4QGyFck3JIgGYRKQt1mNQ23NSlc6wdyk\n'.format(src_ip, src_port)
    str_send += 'From: <sip:34020000002000000001@192.168.1.120:5060>;tag=472039997\n'
    str_send += 'To: <sip:34020000001320000001@3402000000>\n'
    str_send += 'Call-ID: 1141846895\n'
    str_send += 'User-Agent: Monibuca\n'
    str_send += 'CSeq: 1 MESSAGE\n'.format(src_ip, src_port)
    str_send += 'Max-Forwards: 70\n'
    str_send += 'Contact: <sip:34020000002000000001@192.168.1.120:5060>;tag=472039997\n'
    str_send += 'Content-Type: Application/MANSCDP+xml\n'
    str_send += 'Content-Length: 118\n'
    str_send += 'Expires: 3600\n\n'

    body = '<?xml version="1.0"?><Query>\n'
    body += '<CmdType>Catalog</CmdType>\n'
    body += '<SN>1</SN>\n'
    body += '<DeviceID>34020000001320000001</DeviceID>\n'
    body += '</Query>\n\n'

    str_send += body
    print(str_send)
    b4 = str_send.encode()
    s.sendto(b4, (host, port))

def test(s):
    for i in range(5):
        time.sleep(1)
        register(s)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket对象
    # 绑定套接字到源IP地址和端口
    sock.bind((src_ip, src_port))
    # 创建线程
    thread01 = Thread(target=test, args=(sock,), name="线程1")
    # 启动线程
    thread01.start()
    while True:
        data, addr = sock.recvfrom(1024)  # 接收数据
        msg = data.decode()  # 数据从byte格式转出为str
        print('recv----------')
        print(msg)  # 查看接收的数据