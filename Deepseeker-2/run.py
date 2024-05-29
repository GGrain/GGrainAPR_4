import os
import torch
from Rules.samplecodeget import getsamplecode
from Rules.ruledesget import find_rule_description
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


# # 配置代理
# http_proxy = "http://127.0.0.1:4780"
# https_proxy = "https://127.0.0.1:4780"
# socks_proxy = "socks5://127.0.0.1:4781"
#
# # 设置环境变量
# os.environ['HTTP_PROXY'] = http_proxy
# os.environ['HTTPS_PROXY'] = https_proxy
# os.environ['HF_ENDPOINT'] = "https://hf-mirror.com"
# 设置本地模型路径
# Linux
# export HF_ENDPOINT=https://hf-mirror.com
# Windows Powershell
# $env:HF_ENDPOINT = "https://hf-mirror.com"
# 镜像站下载 huggingface-cli download --resume-download deepseek-ai/deepseek-coder-6.7b-instruct --local-dir deepseek-coder
# def func(rule_id,torepaircode):
def deepseeker_repair(rule_id, torepaircode):
    # rule_id = "R-1-2-5"
    # # canprocess = []
    # torepaircode = '''
    # int main(void) {
    #     int array[3] = {0, 1, 2};
    #     int a = 0;
    #     int b = 1;
    #     int c = 2;
    #     if (a+b > c) {  // 违背
    #         printf("a+b>c");
    #     }
    #     return 0;
    # }
    # '''
    json_path = os.path.join(os.path.dirname(__file__), '..', 'rules', 'gjb8114-rule-details.json')
    xml_path = os.path.join(os.path.dirname(__file__), '..', 'rules', 'gjb8114-rules-zh_CN.xml')
    forbidden_code, recommend_code = getsamplecode(rule_id, json_path)
    description = find_rule_description(rule_id, xml_path)
    local_model_path = "../deepseek-coder"
    # 创建 BitsAndBytesConfig 对象，指定量化类型
    quantization_config = BitsAndBytesConfig(load_in_4bit=True)  # 选择 4-bit 量化，也可以使用 load_in_8bit=True 进行 8-bit 量化
    # 加载分词器
    tokenizer = AutoTokenizer.from_pretrained(local_model_path, trust_remote_code=True)
    # 使用 BitsAndBytesConfig 对象加载量化模型
    model = AutoModelForCausalLM.from_pretrained(local_model_path,
                                                 trust_remote_code=True,
                                                 quantization_config=quantization_config,
                                                 torch_dtype=torch.bfloat16,
                                                 device_map='auto')
    # tokenizer = AutoTokenizer.from_pretrained("../deepseek-coder", trust_remote_code=True)
    # model = AutoModelForCausalLM.from_pretrained("../deepseek-coder", trust_remote_code=True,load_in_8bit=True, torch_dtype=torch.bfloat16).cuda()

    torepaircode_ = f'''
    你是一个代码自动规范系统，在接下来的任务中你将参考我给你的规则定义与一对违背示例和遵循示例，
    针对我给你的代码进行修复操作并输出结果，
    注意，尽量在最小范围内修改代码，仅需要输出修复后的代码部分即可，不需要描述
    规则编号: 
    {rule_id}
    规则定义: 
    {description}
    详细说明: 
    违背示例: 
    {forbidden_code}
    遵循示例: 
    {recommend_code}
    待修改代码：
    {torepaircode}
    '''
    content = torepaircode_
    # 只需要输出修改后的代码即可，不需要多余内容
    messages = [
        {'role': 'user', 'content': content}
    ]
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model.device)
    # tokenizer.eos_token_id is the id of <|EOT|> token
    outputs = model.generate(inputs, max_new_tokens=512, do_sample=False, top_k=50, top_p=0.95, num_return_sequences=1,
                             eos_token_id=tokenizer.eos_token_id)
    print(tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True))


if __name__ == '__main__':
    rule_id = "R-1-2-1"
    # canprocess = []
    # torepaircode = '''
    #     int main(void) {
    #         int array[3] = {0, 1, 2};
    #         int a = 0;
    #         int b = 1;
    #         int c = 2;
    #         if (a+b > c) {  // 违背
    #             printf("a+b>c");
    #         }
    #         return 0;
    #     }
    #     '''
    torepaircode = '''
    class Solution {
        public:
            // 按照区间右边界排序
            static bool cmp (const vector<int>& a, const vector<int>& b) {
                return a[1] < b[1];
            }
            int eraseOverlapIntervals(vector<vector<int>>& intervals) {
                if (intervals.size() == 0) return 0;
                sort(intervals.begin(), intervals.end(), cmp);
                int count = 1; // 记录非交叉区间的个数
                int end = intervals[0][1]; // 记录区间分割点
                for (int i = 1; i < intervals.size(); i++)  //违反R-1-2-1
                    if (end <= intervals[i][0]) {
                        end = intervals[i][1];
                        count++;
                    }
                return intervals.size() - count;
            }
        };
    '''
    deepseeker_repair(rule_id, torepaircode)
