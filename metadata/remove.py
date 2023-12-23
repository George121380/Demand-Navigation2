def remove_suffix_and_save(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()

    # 以 .n. 后缀分割每个词
    words = [word.split('.n.')[0] for word in data.split()]

    # 将结果以逗号分隔写入新文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(', '.join(words))

# 替换为你的实际文件路径
input_file_path = '/Users/liupeiqi/工作站/Research/Demand Navigation/GPT4/wnsynsetkey.txt'
output_file_path = 'new_wnsy.txt'

remove_suffix_and_save(input_file_path, output_file_path)


