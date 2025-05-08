import requests
import json

# 读取JSON文件
with open('minsheng.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 高德API密钥
key = "8f27c83768718bc9e350df37c7f8545e"

# 处理数据
for item in data:
    location = item["structured_info"]["地点"]
    location = f"{location}"
    url = f"https://restapi.amap.com/v3/geocode/geo?address={location}&output=json&key={key}"
    response = requests.get(url)
    result = response.json()
    
    if result["status"] == "1":
        location_info = result["geocodes"][0]
        formatted_address = location_info["formatted_address"]
        lng = location_info["location"].split(",")[0]
        lat = location_info["location"].split(",")[1]
        item["structured_info"]["经度"] = lng
        item["structured_info"]["纬度"] = lat
        item["structured_info"]["具体位置"]=formatted_address
    else:
        print(f"Failed to get location for {location}")

# 输出处理后的JSON数据
with open('processed_minsheng.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("处理完成，结果已保存到 processed_minsheng.json 文件中。")