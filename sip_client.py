import socket, random

# 定义源IP地址和端口
src_ip = '192.168.1.10'
src_port = 5061

host = '192.168.1.10'  # 服务端ip
port = 5060  # 服务端ip端口

n = 0

def register(s):
    global n
    str_send = 'REGISTER sip:34020000002000000001@{}:{} SIP/2.0\n'.format(host, port)
    str_send += 'Via: SIP/2.0/UDP {}:{};rport;branch=z9hG4bK{}\n'.format(src_ip, src_port, str(random.randint(10000000000, 99999999999))[1:])
    str_send += 'From: <sip:34020000001320001234@{}:{}>;tag={}\n'.format(src_ip, src_port, str(random.randint(1000000000, 9999999999))[1:])
    str_send += 'To: <sip:34020000001320001234@{}:{}>\n'.format(src_ip, src_port)
    str_send += 'Call-ID: {}\n'.format(str(random.randint(1000000000, 9999999999))[1:])
    n += 1
    str_send += 'CSeq: {} REGISTER\n'.format(str(n))
    str_send += 'Contact: <sip:34020000001320001234@{}:{}>\n'.format(src_ip, src_port)
    str_send += 'Max-Forwards: 70\n'
    str_send += 'User-Agent: NCG V2.6.3.777777\n'
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