import os
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer

# 配置代理
http_proxy = "http://127.0.0.1:4780"
https_proxy = "https://127.0.0.1:4780"
socks_proxy = "socks5://127.0.0.1:4781"

# 设置环境变量
os.environ['HTTP_PROXY'] = http_proxy
os.environ['HTTPS_PROXY'] = https_proxy

# 使用requests库验证代理是否设置成功
try:
    response = requests.get("http://www.google.com", proxies={"http": http_proxy, "https": https_proxy})
    print("HTTP/HTTPS Proxy is working:", response.status_code)
except Exception as e:
    print("Failed to connect through HTTP/HTTPS proxy:", e)