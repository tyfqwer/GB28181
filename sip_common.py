# 定义一个类，表示sip报文，包含首行、头域和消息体三个属性
class SIPMessage:
    # 定义一个构造方法，接受一个参数data，表示sip报文的原始字符串
    def __init__(self, data):
        # 使用split方法按照空行分割data，得到首行和头域部分和消息体部分
        arr = data.split("\r\n\r\n", 1)
        header_part = None
        body_part = None
        if len(arr) == 1:
            header_part = arr[0]
        else:
            header_part = arr[0]
            body_part = arr[1]

        # 使用split方法按照换行符分割首行和头域部分，得到一个列表，列表的第一个元素是首行，后面的元素是头域
        header_list = header_part.split("\n")
        # 将首行赋值给类的首行属性
        self.first_line = header_list[0]
        # 创建一个空字典，用于存储头域的键值对
        self.header_dict = {}
        # 使用一个循环，遍历头域列表，跳过第一个元素（首行）
        for header in header_list[1:]:
            # 使用split方法按照冒号分割头域元素，得到键和值两个部分
            key, value = header.split(":", 1)
            # 去除键和值两个部分的空白字符，并将它们作为键值对添加到字典中
            self.header_dict[key.strip()] = value.strip()
        # 循环结束后，将字典赋值给类的头域属性
        self.header = self.header_dict
        # 将消息体部分赋值给类的消息体属性
        self.body = body_part

    # 从To中获取设备id
    def get_device_id_by_to(self):
        # <sip:34020000001320000001@3402000000>
        to_str = self.header_dict['To']
        display_name, sip_address = to_str.split(":", 1)
        user_name, domain_name = sip_address.split("@", 1)
        user_name = user_name.strip("<>")
        return user_name



data_str = """SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.1.120:15060;branch=z9hG4bK751530395;rport
From: <sip:34020000001320000001@3402000000>;tag=1002450327
To: <sip:34020000001320000001@3402000000>
Call-ID: 1219308817
CSeq: 1 REGISTER
User-Agent: Monibuca
Date: 2023-06-09T14:21:01.339
Content-Length: 0"""

if __name__ == '__main__':
    sip_message = SIPMessage(data_str)
    print(sip_message.first_line)
    print(sip_message.header["Via"])
    print(sip_message.body)
