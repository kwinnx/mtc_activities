import json
from urllib.parse import urljoin

def deduplicate_json(data, baseurl="https://www.icm.gov.mo"):
    # 用于存储去重后的数据
    unique_events = {}
    
    for event in data:
        title = event['title']
        # 如果标题尚未存在，直接添加
        if title not in unique_events:
            unique_events[title] = event
        else:
            # 如果标题已存在，检查 link 是否为 https
            current_event = unique_events[title]
            current_link = current_event['link']
            new_link = event['link']
            
            # 优先保留 https 的记录
            if not current_link.startswith('https://') and new_link.startswith('https://'):
                unique_events[title] = event
    
    # 处理链接，补全非 http 链接
    for title, event in unique_events.items():
        link = event['link']
        if not (link.startswith('https://') or link.startswith('http://')):
            # 使用 urljoin 拼接 baseurl 和相对路径
            event['link'] = urljoin(baseurl, link)
    
    # 转换为列表
    return list(unique_events.values())

# 从 JSON 文件读取数据
input_file = 'wenhua.json'  # 输入 JSON 文件路径
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
except FileNotFoundError:
    print(f"错误：文件 {input_file} 未找到")
    exit(1)
except json.JSONDecodeError:
    print(f"错误：文件 {input_file} 不是有效的 JSON 格式")
    exit(1)

# 执行去重并补全链接
deduplicated_data = deduplicate_json(input_data)

# 输出去重后的结果
print(json.dumps(deduplicated_data, ensure_ascii=False, indent=2))

# 保存到文件
output_file = 'deduplicated_events.json'  # 输出 JSON 文件路径
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(deduplicated_data, f, ensure_ascii=False, indent=2)