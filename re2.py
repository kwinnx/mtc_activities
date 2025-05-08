import requests
from bs4 import BeautifulSoup
import json
import re

def craw_macau_activities(url):
    activity_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = soup.find_all('h2')
    for title in titles:
        a_tag = title.find('a')
        if a_tag:
            print("Title:", a_tag.text.strip())

    # 提取URL
    urls = soup.find_all('url')
    for url in urls:
        print("URL:", url.text.strip())
        
def craw_macau_activities(url):
    activity_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取标题和链接
    articles = soup.find_all('article', class_='cx-row--flat')
    for article in articles:
        title = article.find('h2')
        a_tag = title.find('a')
        if a_tag:
            title_text = a_tag.text.strip()
            title_url = a_tag['href']
            time_str = article.find('div', class_='m-mapitem__list').get('showdate', '')
            # 假设时间格式为 "2025-04-01~2025-04-30"
            start_date, end_date = time_str.split('~')
            activity_list.append({
                'start_date': start_date,
                'end_date': end_date,
                'title': title_text,
                'url': title_url
            })
    
    return activity_list

# 使用函数
url = 'https://www.macaotourism.gov.mo'
activities = craw_macau_activities(url)

# 打印结果
for activity in activities:
    print(activity)



def crawl_detail_page(url):
    try:
        headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
         }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        article_div = soup.find('div', class_='article')
        content = article_div.get_text(strip=True) if article_div else ""

        # 查找所有具有特定class的img标签
        img_tags = soup.find_all('img', class_='nfw-cms-img')
        detail_imgs = []
        for img in img_tags:
            if img.has_attr('src'):
                # 使用正则表达式从src属性中提取图片链接
                match = re.search(r'src="(.*?)"', str(img))
                if match:
                    detail_imgs.append(match.group(1))

        return {
            "content": content,
            "detail_imgs": detail_imgs
        }
    except requests.RequestException as e:
        print(f"请求详情页时出现错误: {e}")
    except Exception as e:
        print(f"解析详情页时出现错误: {e}")
    return {"content": "", "detail_imgs": []}



if __name__ == "__main__":
    base_url = "https://www.hengqin.gov.cn/livelihood/zwdt/hdyg/"
    
    max_page = 6  # 可根据实际情况修改最大页码
    activities = crawl_hengqin_activities(base_url, max_page)
    for activity in activities:
        href = activity["herf"]
        detail_page_content = crawl_detail_page(href)
        activity["detail_imgs"] = detail_page_content["detail_imgs"]
        activity["content"] = detail_page_content["content"]

    # 保存为 JSON 文件
    with open('activities.json', 'w', encoding='utf-8') as f:
        json.dump(activities, f, ensure_ascii=False, indent=4)

    print("数据已保存到 activities.json 文件中。")