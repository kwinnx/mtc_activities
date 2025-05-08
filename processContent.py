from openai import OpenAI
import json
import re

"""
大模型提取详细信息内容
"""

# 初始化客户端
client = OpenAI(
    api_key="eOcxtPgovQbjxvSTkzGZ:pVvgsjxtKrpBbhxabFlh",
    base_url="https://spark-api-open.xf-yun.com/v1"
)

def call_large_model(content):
    messages = [
        {
            "role": "system",
            "content": """请从文本中提取结构化信息，严格按照以下JSON格式返回，不要包含任何其他文本：
            {
                "时间": "",
                "地点": "",
                "活动内容": "",
                "活动主题": ""，
                "主办方":""
            }"""
        },
        {
            "role": "user",
            "content": content
        }
    ]
    
    completion = client.chat.completions.create(
        model='generalv3.5',
        messages=messages
    )
    
    if completion.choices:
        return completion.choices[0].message.content
    return ""

def extract_structured_info(response_content):
    # 尝试直接解析JSON
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        pass
    
    # 尝试提取被```json包裹的内容
    json_match = re.search(r'```json\n(.*?)\n```', response_content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # 如果都不是JSON，尝试从文本中提取
    structured_info = {
        "时间": "",
        "地点": "",
        "活动内容": "",
        "活动主题": "",
        "主办方":""
    }
    
    # 从文本中提取信息
    time_match = re.search(r'时间[：:]\s*(.*?)\n', response_content)
    location_match = re.search(r'地点[：:]\s*(.*?)\n', response_content)
    content_match = re.search(r'活动内容[：:]\s*(.*?)\n', response_content)
    theme_match = re.search(r'活动主题[：:]\s*(.*?)(\n|$)', response_content)
    organization_match = re.search(r'主办方[：:]\s*(.*?)(\n|$)', response_content)
    
    if time_match:
        structured_info["时间"] = time_match.group(1).strip()
    if location_match:
        structured_info["地点"] = location_match.group(1).strip()
    if content_match:
        structured_info["活动内容"] = content_match.group(1).strip()
    if theme_match:
        structured_info["活动主题"] = theme_match.group(1).strip()
    if organization_match:
        structured_info["主办方"] = organization_match.group(1).strip()
    
    return structured_info

def process_activities(activities, output_file):
    structured_activities = []
    for index, activity in enumerate(activities, start=1):
        content = activity.get('content', '').strip()
        if not content:
            print(f"内容为空，跳过处理 (活动 {index}/{len(activities)})")
            continue
        response_content = call_large_model(content)
        print("大模型返回内容:", response_content)
        
        structured_info = extract_structured_info(response_content)
        
        structured_activity = {
            'herf': activity.get('herf', ''),
            '标题': activity.get('标题', ''),
            '图片链接': activity.get('图片链接', ''),
            'detail_imgs': activity.get('detail_imgs', []),
            'class': activity.get('class', ''),
            'original_content': content,
            'structured_info': structured_info
        }
        structured_activities.append(structured_activity)
        # 每处理一个活动，就将结果写入 JSON 文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structured_activities, f, ensure_ascii=False, indent=4)
        print(f"已处理 {index}/{len(activities)} 个活动，结果已保存到 {output_file}")

def main():
    input_file = 'minsheng_all.json'
    output_file = 'minsheng.json'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            activities = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON file: {e}")
        return

    process_activities(activities, output_file)

if __name__ == "__main__":
    main()
