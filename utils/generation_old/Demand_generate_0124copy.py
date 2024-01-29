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
        description=content.get("description","")
        examples=content.get("Examples",[])
        outputfile=content.get("outputfile","")
    return description,examples,outputfile

cats=shuffle_categories('./prompt/habitat_cats_500.txt')

#########################basic prompt##################################
prompt = """You are the owner of a house. I need you to use your imagination and come up with 10 daily demands creatively. 
Each demand should be composed of two parts: a basic demands and your personal preferences. Preferences are supposed to be a subset of base demands, and satisfying preferences necessarily satisfies base demands. I hope you don't mention the needs too vaguely.

Your challenge is to think outside the box and create demands that reflect both necessity and individuality. 
However, remember to keep the demands somewhat open-ended and avoid specifying the use of any particular item from your room.

In your room, you have the following items:
""" 

prompt+=cats
prompt += """
Given these items, generate 10 daily demands. Each demand should follow the format of '<basic demand> + <preferences>'.

Here's a brief description of what I'm looking for:
"""

description,examples,outputfile=read_json_file("RoomComfort")
prompt+=description
prompt+="\n"
prompt += """
To give you an idea, here are some examples:
"""

index=0
for example in examples:
    index+=1
    prompt+=str(index)+"."
    prompt+=example

prompt += """
Now, it's your turn to be creative! Generate diverse demands considering only the items available in your room as mentioned above. Use your imagination, but stay within the realm of everyday practicality. 
I need you to learn the format of the examples above, but don't be too similar to the example or you will be penalized. I will reward you if your answer is very creative. Let's see what unique demands you can come up with!\n"""

post_dict = {
        "model": "gpt-4-1106-preview",
        "messages": [{
              "role": "user",
                "content": prompt
    }],
    "temperature":1.5,
}

r = requests.post("https://frostsnowjh.com/v1/chat/completions", json=post_dict, headers=header)
response_content = r.json()

with open("./dataset/"+outputfile, "a") as file:
        
        file.write(str(current_time) + "\n")
        file.write(response_content['choices'][0]['message']['content'] + "\n"+ "\n")

demands = [{"index": i + 1, "demand": line.strip()} for i, line in enumerate(response_content['choices'][0]['message']['content'].split('\n')) if line.strip()]

# # 将数据写入 JSON 文件
# with open('indexed_demands.json', 'w') as json_file:
#     json.dump(demands, json_file, indent=4)
