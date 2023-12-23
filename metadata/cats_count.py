def count_commas(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            comma_count = content.count(',')
            return comma_count
    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到.")
    except Exception as e:
        print(f"发生错误: {e}")

# 用法示例
file_path = 'super_cat.txt'  # 将 'your_file.txt' 替换为实际的文件路径
result = count_commas(file_path)

if result is not None:
    print(f"文件 '{file_path}' 中逗号的数量为: {result}")
