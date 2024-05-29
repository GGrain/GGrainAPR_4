import os
import torch
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
messages=[
    { 'role': 'user', 'content': "write a quick sort algorithm in python."}
]
inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model.device)
# tokenizer.eos_token_id is the id of <|EOT|> token
outputs = model.generate(inputs, max_new_tokens=512, do_sample=False, top_k=50, top_p=0.95, num_return_sequences=1, eos_token_id=tokenizer.eos_token_id)
print(tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True))
