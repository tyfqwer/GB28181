import socket

# 定义源IP地址和端口
src_ip = '127.0.0.1'
src_port = 5061

host = '127.0.0.1'  # 服务端ip
port = 5060  # 服务端ip端口


def register(s):
    str_send = 'REGISTER sip:34020000002000000001@3402000000 SIP/2.0\n'
    str_send += 'Via: SIP/2.0/UDP 192.168.1.120:5060;rport;branch=z9hG4bK1443727699\n'
    str_send += 'From: <sip:34020000001320000002@3402000000>;tag=474931941\n'
    str_send += 'To: <sip:34020000001320000002@3402000000>\n'
    str_send += 'Call-ID: 732886928\n'
    str_send += 'CSeq: 1 REGISTER\n'
    str_send += 'Contact: <sip:34020000001320000002@192.168.1.120:5060>\n'
    str_send += 'Max-Forwards: 70\n'
    str_send += 'User-Agent: IP Camera\n'
    str_send += 'Expires: 3600\n'
    str_send += 'Content-Length: 0\n\n'
    print(str_send)
    b4 = str_send.encode()
    s.sendto(b4, (host, port))
    print(111)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket对象
    # 绑定套接字到源IP地址和端口
    sock.bind((src_ip, src_port))
    register(sock)
    while True:
        print('send success')
        data, addr = sock.recvfrom(1024)  # 接收数据
        msg = data.decode()  # 数据从byte格式转出为str
        print(msg)  # 查看接收的数据