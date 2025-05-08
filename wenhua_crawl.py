import requests
from bs4 import BeautifulSoup
import json
import re
import os

# 基础URL
base_url = 'https://www.icm.gov.mo'
calendar_url = 'https://www.icm.gov.mo/cn/events/calendar/'  # 事件日历的基础URL

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 存储提取的信息
results = []

# 遍历指定的月份
months = list(range(1, 5))
years = [2023, 2024, 2025]

for year in years:
    for month in months:
        url = f'{calendar_url}{year}/{month}'  # 直接使用月份，不添加前导零

        print(f"正在访问: {url}")  # 打印当前访问的网址

        # 发送HTTP请求获取网页内容
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # 根据网页的编码设置

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找包含事件的div
        rows = soup.find_all('div', class_='rows')
        for row in rows:
            events = row.find_all('div', class_='grid')
            for event in events:
                # 提取图片链接
                image_style = event.find('div', class_='square-box')['style']
                image_url_match = re.findall(r'url\((https?://[^)]+)\)', image_style)
                image_url = image_url_match[0] if image_url_match else None
                
                # 提取链接
                link = None
                link_tag = event.find('div', class_='bTxt').find('a')  # 找到 bTxt 内的 <a> 标签
                if link_tag and link_tag.has_attr('href'):
                    link = link_tag['href']
                else:
                    onclick_script = event.find('div', class_='square-box')['onclick']
                    link_match = re.search(r"window\.location='(.*?)'", onclick_script)
                    link = link_match.group(1) if link_match else None
                
                # 处理相对链接
                if link and not link.startswith(('http://', 'https://')):
                    link = base_url + link

                # 提取标题
                title = link_tag.text.strip() if link_tag else None
                
                # 提取时间
                org_txt_div = event.find('div', class_='orgTxt')
                org_txt = org_txt_div.text.strip() if org_txt_div else None
                
                # 提取地点
                location_p = event.find('p', class_='calendarEventDate')
                location = location_p.text.strip() if location_p else None
                
                # 嵌套爬虫：提取 id="mainContent", id="coreContent" 或 id="container"（不在 footer 内）的文本内容
                main_content = None
                if link:
                    try:
                        # 发送请求获取详情页面
                        detail_response = requests.get(link, headers=headers)
                        detail_response.encoding = 'utf-8'
                        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                        
                        # 查找 id="mainContent" 或 id="coreContent" 的元素
                        content_div = detail_soup.find('div', id='mainContent') or detail_soup.find('div', id='coreContent')
                        
                        # 如果没有找到 mainContent 或 coreContent，查找 id="container"
                        if not content_div:
                            # 获取所有 id="container" 的 div
                            container_divs = detail_soup.find_all('div', id='container')
                            for div in container_divs:
                                # 检查 div 是否在 <footer class="footer"> 内
                                parent_footer = div.find_parent('footer', class_='footer')
                                if not parent_footer:
                                    content_div = div
                                    break  # 取第一个不在 footer 内的 container
                        
                        # 提取文本内容
                        if content_div:
                            main_content = ' '.join(content_div.get_text(strip=True).split())
                        
                    except Exception as e:
                        print(f"无法爬取链接 {link}: {e}")
                
                event_info = {
                    'title': title,
                    'location': location,
                    'time': org_txt,
                    'link': link,
                    'image_url': image_url,
                    'main_content': main_content  # 添加主要内容字段
                }
                results.append(event_info)
            
# 将结果转换为JSON格式
json_results = json.dumps(results, ensure_ascii=False, indent=4)

# 保存结果到wenhua.json文件
with open('wenhua_test.json', 'w', encoding='utf-8') as f:
    f.write(json_results)

print("数据已保存到wenhua_test.json文件")