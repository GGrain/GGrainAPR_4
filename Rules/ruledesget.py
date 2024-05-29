import xml.etree.ElementTree as ET



def find_rule_description(rule_name,file_name):
    # 解析XML文件
    tree = ET.parse(file_name)
    root = tree.getroot()

    # 查找指定规则的描述
    for rule in root.iter('rule'):
        if rule.attrib.get('name') == rule_name:
            return rule.attrib.get('description')
    return None

# # 获取"R-1-2-5"的描述
# # 读取XML文件
# file_name = 'gjb8114-rules-zh_CN.xml'
# rule_description = find_rule_description(file_name, 'R-1-2-5')
# print(rule_description)