import xml.etree.ElementTree as ET

xml_string = """<?xml version="1.0"?>
<Query>
<CmdType>DeviceInfo</CmdType>
<SN>3</SN>
<DeviceID>34020000001320000001</DeviceID>
</Query>"""

if __name__ == '__main__':
    root = ET.fromstring(xml_string)
    print(root.find('CmdType').text.strip())
    print(root.find('DeviceID').text.strip())