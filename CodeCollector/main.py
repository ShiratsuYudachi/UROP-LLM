import requests
from bs4 import BeautifulSoup

# 目标网页URL
url = 'http://example.com'

# 发送GET请求
response = requests.get(url)

# 解析响应内容
soup = BeautifulSoup(response.text, 'html.parser')

# 提取网页的标题
title = soup.find('title').text

print(f'网页标题是：{title}')