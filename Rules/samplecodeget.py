import json


# 定义一个辅助函数，用于清理HTML并转换为代码
def html_to_code(html):
    html = html.replace("&nbsp;", " ")
    html = html.replace("<p style='line-height:0px'>", "")
    html = html.replace("<p style='margin-top:0px;margin-bottom:0px'>", "")
    html = html.replace("</p>", "\n")
    html = html.replace("{\n", "{\n    ")
    html = html.replace("\n}", "    \n}")
    return html.strip()


def getsamplecode(rule_id,file_path='gjb8114-rule-details.json'):
    # 读取JSON文件并解析数据
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 规则标识符
    # rule_id = rule_id

    # 初始化变量
    forbidden_code_html = ""
    recommend_code_html = ""

    # 查找特定规则标识符的条目
    for item in data["details"]:
        if item.get('rule') == rule_id:
            forbidden_code_html = item.get('forbidden', '')
            recommend_code_html = item.get('recommend', '')
            break

    # 转换代码
    forbidden_code = html_to_code(forbidden_code_html)
    recommend_code = html_to_code(recommend_code_html)

    # 输出结果
    # print("Forbidden Code:")
    # print(forbidden_code)
    #
    # print("\nRecommend Code:")
    # print(recommend_code)
    return forbidden_code, recommend_code
