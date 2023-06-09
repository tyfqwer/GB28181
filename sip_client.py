import socket, random
from threading import Thread
import time
import hashlib
from utils import generate_random_string
from sip_common import SIPMessage

# 定义源IP地址和端口
src_ip = '192.168.1.120'
src_port = 15060

host = '192.168.1.120'  # 服务端ip
port = 5060  # 服务端ip端口

device_id = '34020000001320000001'
pwd = '123456'

n = 0


# --------------------------注意必须\r\n结尾，否则m7s解析不出来
def register(s):
    global n
    str_send = 'REGISTER sip:34020000002000000001@3402000000 SIP/2.0\r\n'
    str_send += 'Via: SIP/2.0/UDP {}:{};rport;branch=z9hG4bK{}\r\n'.format(src_ip, src_port, generate_random_string(9))
    str_send += 'From: <sip:{}@3402000000>;tag=1{}\r\n'.format(device_id, generate_random_string(9))
    str_send += 'To: <sip:{}@3402000000>\r\n'.format(device_id)
    str_send += 'Call-ID: 1{}\r\n'.format(generate_random_string(9))
    str_send += 'CSeq: 1 REGISTER\r\n'
    str_send += 'Contact: <sip:{}@{}:{}>\r\n'.format(device_id, src_ip, src_port)
    str_send += 'Max-Forwards: 70\r\n'
    str_send += 'User-Agent: IP Camera\r\n'
    str_send += 'Expires: 3600\r\n'
    str_send += 'Content-Length: 0\r\n\r\n'
    print(str_send)
    b4 = str_send.encode()
    s.sendto(b4, (host, port))


# 注册认证
def register_auth(s, msg):
    global n
    str_send = 'REGISTER sip:34020000002000000001@3402000000 SIP/2.0\r\n'
    str_send += 'Via: SIP/2.0/UDP {}:{};rport;branch=z9hG4bK{}\r\n'.format(src_ip, src_port, generate_random_string(9))
    str_send += 'From: <sip:{}@3402000000>;tag=1{}\r\n'.format(device_id, generate_random_string(9))
    str_send += 'To: <sip:{}@3402000000>\r\n'.format(device_id)
    str_send += 'Call-ID: 1{}\r\n'.format(generate_random_string(9))
    str_send += 'CSeq: 1 REGISTER\r\n'
    str_send += 'Contact: <sip:{}@{}:{}>\r\n'.format(device_id, src_ip, src_port)

    www_authenticate = msg.header_dict['WWW-Authenticate']
    auth_list = www_authenticate.split()  # 按照空格分割
    auth_scheme, auth_str = auth_list
    auth_dict = {}
    for item in auth_str.split(','):
        print(item)
        key, value = item.split('=')  # 按照等号分割每个元素
        value = value.strip("\"")  # 去除属性值两端的引号
        auth_dict[key] = value
    # 验证算法
    # HA1=MD5 (username:realm:passwd) #username 和 realm 在字段 “Authorization” 中可以找到，passwd 这个是由客户端和服务器协商得到的，一般情况下 UAC 端存一个 UAS 也知道的密码就行了
    # HA2=MD5 (Method:Uri) #Method 一般有 INVITE, ACK, OPTIONS, BYE, CANCEL, REGISTER；Uri 可以在字段 “Authorization” 找到
    # response = MD5(HA1:nonce:HA2)
    uri = 'sip:{}@3402000000'.format(device_id)
    ha1_str = device_id + ':' + auth_dict['realm'] + ':' + pwd
    ha1 = hashlib.md5(ha1_str.encode()).hexdigest()
    ha2_str = 'REGISTER:' + uri
    ha2 = hashlib.md5(ha2_str.encode()).hexdigest()
    response_str = ha1 + ':' + auth_dict['nonce'] + ':' + ha2
    response = hashlib.md5(response_str.encode()).hexdigest()
    www_authenticate += ',username="{}"'.format(device_id)
    www_authenticate += ',response="{}"'.format(response)
    www_authenticate += ',uri="{}"'.format(uri)
    str_send += 'Authorization: {}\r\n'.format(www_authenticate)

    str_send += 'Max-Forwards: 70\r\n'
    str_send += 'User-Agent: IP Camera\r\n'
    str_send += 'Expires: 3600\r\n'
    str_send += 'Content-Length: 0\r\n\r\n'
    print(str_send)
    b4 = str_send.encode()
    s.sendto(b4, (host, port))


# 设备状态信息报送 心跳监测
def heartbeat_monitor(s):
    while True:
        body = '<?xml version="1.0" encoding="UTF-8"?>\r\n'
        body += '<Notify>\r\n'
        body += '<CmdType>Keepalive</CmdType>\r\n'
        body += '<SN>43</SN>\r\n'
        body += '<DeviceID>{}</DeviceID>\r\n'.format(device_id)
        body += '<Status>OK</Status>\r\n'
        body += '</Notify>\r\n\r\n'
        str_send = 'MESSAGE sip:34020000002000000001@3402000000 SIP/2.0\r\n'
        str_send += 'Via: SIP/2.0/UDP {}:{};rport;branch=z9hG4bK{}\r\n'.format(src_ip, src_port, generate_random_string(9))
        str_send += 'From: <sip:{}@3402000000>;tag=1{}\r\n'.format(device_id, generate_random_string(9))
        str_send += 'To: <sip:{}@3402000000>\r\n'.format(device_id)
        str_send += 'Call-ID: 1{}\r\n'.format(generate_random_string(9))
        str_send += 'CSeq: 2 MESSAGE\r\n'
        str_send += 'Contact: <sip:{}@{}:{}>\r\n'.format(device_id, src_ip, src_port)
        str_send += 'Content-Type: Application/MANSCDP+xml\r\n'
        str_send += 'Max-Forwards: 70\r\n'
        str_send += 'User-Agent: IP Camera\r\n'
        str_send += 'Content-Length: {}\r\n\r\n'.format(len(body))
        str_send += body
        print(str_send)
        b4 = str_send.encode()
        s.sendto(b4, (host, port))
        time.sleep(60)


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


def monitor_messages(s):
    while True:
        data, addr = sock.recvfrom(1500)  # 接收数据
        msg = data.decode()  # 数据从byte格式转出为str
        print('recv----------')
        print(msg)
        sip_msg = SIPMessage(msg)
        device_no = sip_msg.get_device_id_by_to()
        csep = sip_msg.header_dict['CSeq']
        num, msg_type = csep.split(' ')
        if msg_type == 'REGISTER':
            if sip_msg.first_line.find('401 Unauthorized') != -1:
                register_auth(s, sip_msg)
            elif sip_msg.first_line.find('200 OK') != -1:
                # 创建线程
                heartbeat_thread = Thread(target=heartbeat_monitor, args=(sock,), name="heartbeat_thread")
                # 启动线程
                heartbeat_thread.start()
                print('注册成功')
            else:
                print('不支持的内容：{}'.format(sip_msg.first_line))
        elif msg_type == 'MESSAGE':
            if sip_msg.first_line.find('200 OK') != -1:
                print('MESSAGE 200 OK')
        else:
            print("不支持的类型：{}".format(msg_type))


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket对象
    # 绑定套接字到源IP地址和端口
    sock.bind((src_ip, src_port))
    # 创建线程
    thread01 = Thread(target=monitor_messages, args=(sock,), name="线程1")
    # 启动线程
    thread01.start()

    time.sleep(1)
    register(sock)

    time.sleep(2000)
