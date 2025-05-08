import json

def remove_duplicates(file_path):
    try:
        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("文件未找到，请检查路径。")
        return
    except json.JSONDecodeError:
        print("JSON 文件格式错误。")
        return

    # 创建一个字典用于去重
    seen = {}
    unique_data = []
    deleted_count = 0  # 用于统计被删除的数据数量

    for item in data:
        original_content = item.get('original_content', '')
        if original_content and original_content not in seen:
            seen[original_content] = True
            unique_data.append(item)
        else:
            deleted_count += 1  # 如果内容重复，则增加删除计数

    # 写回 JSON 文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)

    # 打印结果
    print(f"去重完成，结果已写入文件。")
    print(f"被删除的重复数据数量：{deleted_count}")

# 示例调用
file_path = 'processed_minsheng.json'
remove_duplicates(file_path)