import os
import requests
import json
from tqdm import tqdm
import random   
import pandas as pd
import re


def id_2_cat():
    df = pd.read_csv("/Users/liupeiqi/工作站/Research/Demand Navigation/Demand-driven-navigation-Plus/dataset_generation/metadata/habitat_objects.csv")
    obj_id = df['id'].to_list()
    name=df['wnsynsetkey'].to_list()
    id_to_name=dict(zip(obj_id,name))
    set_name=list(set(name)) 
    return id_to_name,set_name

def scene_cat(scene_path):
    json_file_name = os.path.basename(scene_path)
    with open(scene_path) as f:
        scene=json.load(f)
        id_to_name,set_name=id_2_cat()
    obj_list_in_scene=set([id_to_name[scene['object_instances'][i]['template_name'].split("_")[0]] for i in range(len(scene['object_instances'])) ])
    return obj_list_in_scene,json_file_name

def inf_record(obj_list,json_file_name):
    lens=len(obj_list)
    txt_file_path = '/Users/liupeiqi/工作站/Research/Demand Navigation/Demand-driven-navigation-Plus/dataset_generation/scene_data/information_record.txt'
    with open(txt_file_path, 'a') as txt_file:
        txt_file.write(f"JSON File Name: {json_file_name}\n")
        txt_file.write(f"List Length: {lens}\n")
        txt_file.write("List Contents:\n")
        txt_file.write(f"{obj_list}\n")

def filter_objects(scene_items, task_data):
    with open(task_data) as f:
        task_data=json.load(f)
    # 将字符串转换为集合
    scene_items_set = set(scene_items)

    # 过滤函数，检查所有物品是否都在场景中
    def all_items_present(item_list):
        return all(item in scene_items_set for item in item_list)

    # 过滤basic_object和preference_object
    filtered_basic_objects = [obj for obj in task_data["basic_object"] if all_items_present(obj)]
    filtered_preference_objects = [obj for obj in task_data["preference_object"] if all_items_present(obj)]

    return filtered_basic_objects, filtered_preference_objects

def extract_and_save_json(text):
    # 使用正则表达式匹配 JSON 格式的文本
    matches = re.findall(r'\{[^{}]*\}', text)
    
    for match in matches:
        try:
            # 尝试解析匹配到的文本为 JSON
            json_data = json.loads(match)

            # 检查关键字段是否存在
            if all(key in json_data for key in ["task_instruction", "basic_demand", "preference", "basic_object", "preference_object"]):
                # 将 JSON 数据写入文件
                try:
                    with open("./Dataset_lpq/output.json", 'r', encoding='utf-8') as file:
                        source_data = json.load(file)
                except json.JSONDecodeError:
                    # 如果文件为空或无法解析，返回空数组
                    source_data= []
               
                source_data.append(json_data)

                with open("./Dataset_lpq/output.json", 'w') as file:
                    json.dump(source_data, file, indent=4)
                return
        except json.JSONDecodeError:
            # 如果解析失败，继续检查下一个匹配项
            continue

    print("No valid JSON found in the text")

def askGPT(system_prompt,prompt):
    gpt_key = open("key.txt", "r").read().strip()
    header = {
        "Content-Type":"application/json",
        "Authorization": f"Bearer {gpt_key}",
        # "Organization": "org-PmiFO2CwwRvqBO0UpCYfKqgs"
    }

    post_dict = {
            "model": "gpt-4-1106-preview",
            "messages": [{
                    "role": "system",
                    "content": system_prompt,
                    "role": "user",
                    "content": prompt,
            }],
            # "temperature": 1.99,
            
    }
    r = requests.post("https://frostsnowjh.com/v1/chat/completions", json=post_dict, headers=header)
    return r

def demand_demo():
    df = pd.read_csv("metadata/habitat_objects.csv")
    obj_id = df['id'].to_list()
    name=df['wnsynsetkey'].to_list()
    id_to_name=dict(zip(obj_id,name))
    set_name=list(set(name))
    # obj_list_in_scene=set()
    # all_scene=os.listdir(os.path.join(path,"scenes"))
    # for scene_json in tqdm(all_scene):
    #     with open(os.path.join(path,"scenes",scene_json)) as f:
    #         scene=json.load(f)
    #     obj_list_in_scene=obj_list_in_scene.union(set([id_to_name[scene['object_instances'][i]['template_name'].split("_")[0]] for i in range(len(scene['object_instances'])) ]))
    
    data=[]
    num=0
    total_iterations=10
    pbar = tqdm(total=total_iterations)
    while True:
        try:
            random.shuffle(set_name)
            set_name=set_name[:200]
            object_prompt='The object categories in the scenes are: '
            for obj_name in set_name:
                if isinstance(obj_name,str):
                    object_prompt+=obj_name+', '
                    
            system_prompt="You are an AI assistant that can understand human demands and imagine what human demands can be met with existing object categories."
            prompt='''
            ###Start Instruction###
            Generate a task for demand-driven navigation. The task should involve an agent finding an object within the specified category that meets the given demands and preferences.

            ###Object Category###
            '''+object_prompt+'''

            ###Demand-driven Navigation Task Template###
            {
                "task_instruction": $basic_demand$, $preference$
                "basic_demand": xxx
                "preference": xxx
                "basic_object": [[object_g],[object_a, object_c, object_d],[object_b, object_c, object_e],[object_b, object_f]]
                "preference_object": [[object_a, object_c, object_d], [object_b, object_f]]
            }
            This shoule be in dict format.
            basic_object is a list whose elements are lists, and each element represents a solution that meets the basic_demand; each solution may consist of one or more objects.
            preference_object is a list whose elements are lists, and each element represents a solution that meets both the basic_demand and preference; each solution may consist of one or more objects.
            "[object_g]" represents that just object_g can meet the demand.
            "[object_x, object_y, object_z]" represents that only the combination of object x, y, and z can meet the demand.
            As you can see, preference_object must be a subset of basic_object. So if an object solution is in preference_object, it must also be in basic_object.
            
            ###Example 1###
            "task_instruction":"I want to listen to music, but I don't want the sound to disturb myfamily."
            "basic_demand": "I want to listen to music"
            "preference": "but I don't want the sound to disturb myfamily"
            "basic_object": ["audio_system"],["radio_receiver"],["record_player"],["loudspeaker"],["media_player"],["headphone","media_player"],["laptop"],["laptop","headphone"],["tablet_computer"],["tablet_computer","headphone"],["cellular_telephone"],["headphone","cellular_telephone"]
            "preference_object": ["headphone","cellular_telephone"],["tablet_computer","headphone"],["tablet_computer","headphone"]
        
            ###Final Instruction###
            You need to use the above task template to generate the corresponding demand and object that can meet the demands. \'Basic_object only need to meet the requirements stated in basic demand, while preference objects need to meet the requirements in both basic demand and preference.
            It should be noted that the object must be within the Object Category.
            You should not explain anything, just generate the task.
            after you generate "basic_demand" and "preference", you should think step by step about how to generate "basic_object" and "preference_object".
            And finally, you should format your reponse into the Demand-driven Navigation Task Template.
            
            '''
            r=askGPT(system_prompt,prompt)
            responses=r.json()['choices'][0]['message']['content']
            
            responses=responses.split("=========")
            for task in responses:
                if task != '':
                    data.append(json.loads(task))
                    num+=1
                    pbar.update(1)
            with open("./nocat_demo.json",'w') as f:
                json.dump(data,f,indent=4)
            if num>=total_iterations:
                break
        except Exception as e:
            print(e)
            continue
    
def refine():
    path="./habitat-lab/data/scene_datasets/hssd-hab"
    df = pd.read_csv("/Users/liupeiqi/工作站/Research/Demand Navigation/GPT4/metadata/habitat_objects.csv")
    obj_id = df['id'].to_list()
    name=df['wnsynsetkey'].to_list()
    id_to_name=dict(zip(obj_id,name))
    set_name=list(set(name)) 
    
    with open("./nocat_demo.json",'r') as f:
        data=json.load(f)
    random.shuffle(set_name)
    # set_name=set_name[:200]
    object_prompt='The object categories in the scenes are: '
    total_len=len(data)
    pbar = tqdm(total=total_len)
    for obj_name in set_name:
        if isinstance(obj_name,str):
            object_prompt+=obj_name+', '
    for task in data:
        prompt='''
        ###Start Instruction###
           Check whether the task is reasonable. If it is unreasonable, please modify it to make it reasonable.
        ###Object Category###
        '''+object_prompt+'''
        ###Demand-driven Navigation Task Template###
        {
            "task_instruction": $basic_demand$, $preference$
            "basic_demand": xxx
            "preference": xxx
            "basic_object": [[object_g],[object_a, object_c, object_d],[object_b, object_c, object_e],[object_b, object_f]]
            "preference_object": [[object_a, object_c, object_d], [object_b, object_f]]
        }
        This shoule be in dict format.
        basic_object is a list whose elements are lists, and each element represents a solution that meets the basic_demand; each solution may consist of one or more objects.
        preference_object is a list whose elements are lists, and each element represents a solution that meets both the basic_demand and preference; each solution may consist of one or more objects.
        "[object_g]" represents that just object_g can meet the demand.
        "[object_x, object_y, object_z]" represents that only the combination of object x, y, and z can meet the demand.
        As you can see, preference_object must be a subset of basic_object. So if an object solution is in preference_object, it must also be in basic_object.
        ###To be modified Task in JSON String Format###
        ''' + json.dumps(task) + '''
        ### Final Instruction ###

        First, you need to check if there are other items in the Object Category I provided that can meet the basic_demand and preference. If there are, add them to the basic_object and preference_object.
        Then, you need to determine whether each combination solution (i.e., [object_a, object_c, object_d] or [object_b, object_c, object_e]) in basic_object can fully meet basic_demand, and whether removing one object from a solution would result in it no longer satisfying basic_demand.
        And whether each combination solution (i.e., [object_a, object_c, object_d]) in preference_object can fully meet basic_demand and preference, and whether removing one object from a solution would result in it no longer satisfying basic_demand and preference.
        Your reply should first briefly explain the irrational aspects, and then provide a remedial plan. Note that the objects mentioned in the remedial plan should also be included in the Object Category and must conform to the Demand-driven Navigation Task Template.
        Your can use objects in the Object Category to replace the objects in the original task, or add objects to the original task.
        Finally, check if "preference_object" is a subset of "basic_object", meaning every combination solutions in "preference_object" must be included in "basic_object". If not, you have to write the those extra combination solutions into "basic_object".
        '''
        system_prompt="""You are an AI assistant that can help check whether objects meet the demands, equipped with common life knowledge. Your reply should be in JSON string format. You should not explain anything, just generate your response in following format:
        {
            "reason": xxx
            "refined_task": xxx
            "explain": xxx
        }"""
        r=askGPT(system_prompt,prompt)
        responses=r.json()['choices'][0]['message']['content']
        t=1
        print(responses)
        extract_and_save_json(responses)
        pbar.update(1)


if __name__ == "__main__":
    #demand_demo()
    #refine()
    objlist,json_file_name=scene_cat("/Users/liupeiqi/工作站/Research/Demand Navigation/Demand-driven-navigation-Plus/dataset_generation/scene_data/106366371_174226743.scene_instance.json")
    inf_record(objlist,json_file_name)
    print(objlist)
    task_path="/Users/liupeiqi/工作站/Research/Demand Navigation/Demand-driven-navigation-Plus/dataset_generation/Dataset_lpq/test.json"
    
    basic_objects,prefered_objects=filter_objects(objlist,task_path)
    print("Found Basic Objects:", basic_objects)
    print("Found Preference Objects:", prefered_objects)

