import requests
from bs4 import BeautifulSoup
import json

def get_page_content(url):
    """通过活动链接获取页面内容"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # 返回原始HTML内容
    return None

def parse_activity_detail_v2(activity):
    """解析活动详细页面，并动态提取描述信息"""
    activity_url = activity['活动链接']
    activity_content = get_page_content(activity_url)
    
    if activity_content:
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(activity_content, 'html.parser')
        
        # 提取图片链接 (例如：gallery)
        gallery_images = soup.find_all('script', string=lambda text: text and 'gallery' in text)
        image_links = []
        for script in gallery_images:
            if "gallery" in script.string:
                start = script.string.find('gallery') + len('gallery') + 2
                end = script.string.find(']', start)
                images = script.string[start:end].strip().split(',')
                for image in images:
                    image = image.replace('\\', '/').strip('[]"')
                    image_links.append(image)
        
        # 提取活动内容 (活动描述)，查找所有带有direction: ltr样式的元素
        activity_description = ""  # 初始化描述内容
        elements_with_ltr_style = soup.find_all(style=lambda value: value and 'direction: ltr' in value)
        for element in elements_with_ltr_style:
            # 提取文本内容
            text = element.get_text(strip=True)
            if text:
                activity_description = text  # 更新活动描述内容
                break  # 假设第一个找到的符合条件的文本就是活动描述
        
        # 提取地点信息 (例如：location)
        location_info = soup.find_all('script', string=lambda text: text and 'coordinate' in text)
        location_data = []
        for script in location_info:
            if "coordinate" in script.string:
                start = script.string.find('coordinate') + len('coordinate') + 3
                end = script.string.find(']', start)
                coordinates = script.string[start:end].strip().split(',')
                coordinates = [coord.strip('\"') for coord in coordinates]  # 去掉多余的双引号
                # 动态获取地点名称
                location_name_start = script.string.find('name') + len('name') + 2
                location_name_end = script.string.find('",', location_name_start)
                location_name = script.string[location_name_start:location_name_end].strip() if location_name_start != -1 else "未知地点名称"
                location_data.append({'name': location_name, 'coordinate': coordinates})
        
        # 更新活动信息
        activity['图片链接'] = image_links
        activity['活动内容'] = activity_description
        activity['地点名称'] = location_data[0]['name'] if location_data else "未知地点名称"
        activity['经度'] = location_data[0]['coordinate'][0] if location_data else "未知经度"
        activity['纬度'] = location_data[0]['coordinate'][1] if location_data else "未知纬度"
    
    return activity



def main():
    # 假设这是从第一阶段获取的活动列表
    activities_info = [
        {
            "活动名称": "佐贝伊德之上－第六十届威尼斯国际艺术双年展澳门作品展",
            "活动ID": "11493",
            "活动日期范围": "2025-04-01,2025-04-30",
            "活动标签": "佐贝伊德之上－第六十届威尼斯国际艺术双年展澳门作品展",
            "活动状态": "未知状态",
            "活动描述": "未知活动描述",
            "活动链接": "https://www.macaotourism.gov.mo/zh-hans/events/whatson/11493"
        },
        {
            "活动名称": "炫耀 3.0：露施雅、左凯士及孟丽泰之艺术收藏展",
            "活动ID": "11526",
            "活动日期范围": "2025-04-01,2025-04-30",
            "活动标签": "炫耀 3.0：露施雅、左凯士及孟丽泰之艺术收藏展",
            "活动状态": "未知状态",
            "活动描述": "未知活动描述",
            "活动链接": "https://www.macaotourism.gov.mo/zh-hans/events/whatson/11526"
        }
    ]
    
    # 对每个活动的详细页面进行爬取
    for activity in activities_info:
        print(f"正在处理活动: {activity['活动名称']}")
        parse_activity_detail_v2(activity)
    
    # 将所有活动信息保存为JSON文件
    with open('activities_detail.json', 'w', encoding='utf-8') as f:
        json.dump(activities_info, f, ensure_ascii=False, indent=4)
    
    print("所有活动的详细信息已保存到 activities_detail.json 文件中。")

if __name__ == "__main__":
    main()