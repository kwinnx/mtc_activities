import requests
from bs4 import BeautifulSoup
import json
import re

"""
爬取民生事务局
"""

def crawl_hengqin_activities(base_url, max_page=10):
    activity_list = []
    for page in range(1, max_page + 1):
        url = base_url + 'index.html' if page == 1 else base_url + f'index_{page}.html'
        try:
             headers = {
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
             }
             response = requests.get(url, headers=headers)
             response.raise_for_status()
             soup = BeautifulSoup(response.text, 'html.parser')

             news_items = soup.select('ul.news_list li')
             for item in news_items:
                 try:
                     href = item.find('a')['href']
                     title = item.find('div', class_='hascover').find('p').text if item.find('div', class_='hascover') else ''
                     time = item.find('div', class_='hascover').find_all('p')[-1].text if item.find('div', class_='hascover') else ''
                     img = item.find('div', class_='r_img')
                     img_src = img.find('img')['src'] if img and img.find('img') else ''

                     activity = {
                         "herf": href,
                         "活动标题": title,
                         "发布时间": time,
                         "首页图片链接": img_src
                     }
                     activity_list.append(activity)
                 except (AttributeError, KeyError) as e:
                     print(f"解析单个活动项时出现错误: {e}，当前活动项: {item}")
        except requests.RequestException as e:
             print(f"请求第 {page} 页时出现错误: {e}")
        except Exception as e:
             print(f"处理第 {page} 页时发生未知错误: {e}")

    return activity_list

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
    base_url = "https://www.hengqin.gov.cn/livelihood/msgk/qncy/gk/zwdt/"
    #https://www.hengqin.gov.cn/livelihood/msgk/ylws/gk/zwdt/医疗卫生活动 14页
    #https://www.hengqin.gov.cn/livelihood/msgk/jyzy/gk/zwdt/讲座及教育活动 15页
    #https://www.hengqin.gov.cn/tmsswj/msgk/sbfw/gk/zwdt/社会保障活动 20页
    #https://www.hengqin.gov.cn/livelihood/msgk/whss/zwdt/ 文化体育活动 20页
    #https://www.hengqin.gov.cn/livelihood/msgk/qncy/gk/zwdt/index_9.html 澳门青年服务相关活动 9页


    
    max_page = 9  # 可根据实际情况修改最大页码
    activities = crawl_hengqin_activities(base_url, max_page)
    for activity in activities:
        href = activity["herf"]
        detail_page_content = crawl_detail_page(href)
        activity["detail_imgs"] = detail_page_content["detail_imgs"]
        activity["content"] = detail_page_content["content"]
        activity["class"] = "澳门青年服务相关活动"
        

    # 保存为 JSON 文件
    with open('activities_qingnian.json', 'w', encoding='utf-8') as f:
        json.dump(activities, f, ensure_ascii=False, indent=4)

    print("数据已保存到 activities.json 文件中。")