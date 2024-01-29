# !/usr/bin/env python
import requests
import re
from datetime import datetime
import json
import random

current_time = datetime.now()
header = {
        "Content-Type":"application/json",
        "Authorization": "Bearer fa-YjAyODMwNjgtZDE3YS00MjU1LWIzZDQtZmNmOWFiNDQ0ZmUzMTY5NzUyODgzNjAx"
}
##################################TO DO##################################
#cat input 每次输入时打乱

def shuffle_categories(file_path):
    # 读取文件内容
    with open(file_path, 'r') as file:
        categories_text = file.read().strip()

    # 将文本按逗号分割成类别列表
    categories_list = categories_text.split(', ')

    # 随机打乱类别列表
    random.shuffle(categories_list)

    # 将打乱后的类别列表连接成字符串
    shuffled_categories_text = ', '.join(categories_list)

    # 输出结果
    print("原始类别顺序:", categories_text)
    print("打乱后的类别顺序:", shuffled_categories_text)
    return shuffled_categories_text

def read_json_file(demand_cat,file_path="./prompt/Demand_classification.json"):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        content=json_data.get(demand_cat,{})
        discritption=content.get("discritption","")
        examples=content.get("Examples",[])
        outputfile=content.get("outputfile","")
    return discritption,examples,outputfile

cats=shuffle_categories('./prompt/habitat_cats_500.txt')

#########################basic prompt##################################
prompt="""You are the owner of a house. And I need you to generate 10 daily demands creatively.\n """
prompt+="""You have those things in your room:\n"""
prompt=cats
prompt+="""Base on those things in your room, generate 10 daily demands for me. Note that The demand should be seperate into two parts:<basic demand>+< preferences>. """

prompt+="""Present a less specific demand and try not to specify the use of a particular item."""

prompt+="""Here are some examples:"""

examples_hard="""
---
1.I am thirsty, and I want to drink something sweet.\n
2.I want to decorate my room, maybe I can put something on the wall.\n
3.I need to wash my clothes, but the soap is hard to use.\n
4.I want to listen to some music, it will be better to have some device that allows me to share the music with my friends.\n
5.I am bored ,Can I play any ball games?\n
---
"""

examples_one="""
---
1.I am thirsty, and I want to drink something sweet.\n

2.I need to wash my clothes, but the soap is hard to use.\n
---
"""

prompt+=examples_one

prompt+="""Refer to these examples, generate diverse demands for me. Try to be creative!\n"""

post_dict = {
        "model": "gpt-4-0613",
        "messages": [{
              "role": "user",
                "content": prompt
    }]
}

r = requests.post("https://frostsnowjh.com/v1/chat/completions", json=post_dict, headers=header)
response_content = r.json()

with open("./dataset/demands.txt", "a") as file:
        
        file.write(str(current_time) + "\n")
        file.write(response_content['choices'][0]['message']['content'] + "\n"+ "\n")

demands = [{"index": i + 1, "demand": line.strip()} for i, line in enumerate(response_content['choices'][0]['message']['content'].split('\n')) if line.strip()]

# # 将数据写入 JSON 文件
# with open('indexed_demands.json', 'w') as json_file:
#     json.dump(demands, json_file, indent=4)
