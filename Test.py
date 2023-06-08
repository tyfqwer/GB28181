import socket

host = '127.0.0.1'  # 服务端ip
port = 5060  # 服务端ip端口

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket对象
    sock.bind((host, port))  # 根据服务端地址，建立连接
    while True:
        data, addr = sock.recvfrom(1024)  # 接收数据
        msg = data.decode()  # 数据从byte格式转出为str
        print(msg)  # 查看接收的数据