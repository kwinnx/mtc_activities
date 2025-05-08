from openai import OpenAI
import json
import re

# 初始化客户端  换成你的api和url
client = OpenAI(
    api_key="QdYdoJjsnGnkIhCdjFOE:wzplLPokFRJSlxXNIqnj",
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
                "主办方": ""，
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
        "主办方": "",
        "活动主题": ""
        }
    
    # 从文本中提取信息
    time_match = re.search(r'时间[：:]\s*(.*?)\n', response_content)
    location_match = re.search(r'地点[：:]\s*(.*?)\n', response_content)
    content_match = re.search(r'活动内容[：:]\s*(.*?)\n', response_content)
    theme_match = re.search(r'活动主题[：:]\s*(.*?)(\n|$)', response_content)
    organizations = re.search(r'主办方[：:]\s*(.*?)\n', response_content)
    
    if time_match:
        structured_info["时间"] = time_match.group(1).strip()
    if location_match:
        structured_info["地点"] = location_match.group(1).strip()
    if content_match:
        structured_info["活动内容"] = content_match.group(1).strip()
    if theme_match:
        structured_info["活动主题"] = theme_match.group(1).strip()
    if organizations:
        structured_info["主办方"] = theme_match.group(1).strip()
    
    return structured_info

def process_activities(activities):
    structured_activities = []
    for activity in activities:
        content = activity.get('content', '')
        response_content = call_large_model(content)
        print("大模型返回内容:", response_content)
        
        structured_info = extract_structured_info(response_content)
        
        structured_activity = {
            'herf': activity.get('herf', ''),
            '标题': activity.get('标题', ''),
            '图片链接': activity.get('图片链接', ''),
            'detail_imgs': activity.get('detail_imgs', []),
            'original_content': content,
            'structured_info': structured_info
        }
        structured_activities.append(structured_activity)
    return structured_activities

def main():
    try:
        #读json文件 进行处理
        with open('activities.json', 'r', encoding='utf-8') as f:
            activities = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON file: {e}")
        return

    structured_activities = process_activities(activities)
    if structured_activities:
        with open('structured_activities.json', 'w', encoding='utf-8') as f:
            json.dump(structured_activities, f, ensure_ascii=False, indent=4)
        print("结构化数据已保存到 structured_activities.json 文件中。")
    else:
        print("No activities processed.")

if __name__ == "__main__":
    main()