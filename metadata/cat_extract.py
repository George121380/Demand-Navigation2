import json

def extract_main_categories_and_save_to_txt(json_file_path, output_file):
    unique_categories = set()

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for entry in data:
            main_category = entry.get("main_wnsynsetkey", "")
            if main_category:
                unique_categories.add(main_category)

    # 写入文本文件
    with open(output_file, 'w', encoding='utf-8') as txt_file:
        txt_file.write(', '.join(unique_categories))

json_file_path = '/Users/liupeiqi/工作站/Research/Demand Navigation/GPT4/habitat_all_useful_inf.json'  # 替换为你的 JSON 文件路径
output_file = 'main_wnsynsetkey.txt'   # 输出文本文件路径

extract_main_categories_and_save_to_txt(json_file_path, output_file)
