from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

"""
爬取澳门旅游官网代码 
"""

def crawl_hengqin_activities(url):
    try:
        """
        # 设置Chrome选项
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")

        # 初始化Chrome WebDriver
        service = Service(executable_path='C:\\Users\\user\\chromedriver\\chromedriver.exe')  # 替换为您的chromedriver路径
        driver = webdriver.Chrome(service=service, options=options)

        # 打开网页
        driver.get(url)

        # 等待页面加载完成
        wait = WebDriverWait(driver, 10)  # 设置最长等待时间
        element = (By.CSS_SELECTOR, 'div#map-intro')  # 替换为实际的CSS选择器
        wait.until(EC.presence_of_element_located(element))
        
        # 获取页面内容
        page_content = driver.page_source
        
        # 关闭浏览器
        driver.quit()

        # 保存页面内容到txt文件
        with open('page_content.txt', 'w', encoding='utf-8') as f:
            f.write(page_content)
        """


        with open('page_content.txt', 'r', encoding='utf-8') as f:
            page_content = f.read()


        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(page_content, 'html.parser')

        # 找到所有活动的容器
        activities = soup.find_all('div', class_=lambda x: x and 'cx-div' in x and 'm-mapitem__list' in x)

        # 找到所有活动的容器
        #activities = soup.find_all('div', class_='cx-div m-mapitem__list' )

        # 创建一个列表来存储所有活动的信息
        activities_info = []

        # 遍历每个活动并提取信息
        for activity in activities:
            # 提取活动名称
            activity_name_element = activity.find('a', class_='stretched-link')
            activity_name = activity_name_element.text.strip() if activity_name_element else "未知活动名称"
            
            # 提取活动ID
            activity_id = activity.get('id') if activity.get('id') else "未知活动ID"
            
            # 提取活动日期范围
            event_date_range = activity.get('eventdaterange') if activity.get('eventdaterange') else "未知日期范围"
            
            # 提取活动标签
            aria_label = activity.get('aria-label') if activity.get('aria-label') else "未知活动标签"
            
            # 提取活动状态
            date_status_element = activity.find('span', class_='date-status--ended')
            
            date_status = date_status_element.text.strip() if date_status_element else "未知状态"
            
            # 提取活动描述
            activity_description_element = activity.find('p', style="direction: ltr")
            #print(aria_label +'中间打印结果'+ date_status_element +'中间打印结果'+ activity_description_element)
            activity_description = activity_description_element.text.strip() if activity_description_element else "未知活动描述"

            # 构造活动链接
            base_url = "https://www.macaotourism.gov.mo/zh-hans/events/whatson/"
            activity_link = f"{base_url}{activity_id}"

            # 将提取的信息存储为一个字典
            activity_info = {
                "活动名称": activity_name,
                "活动ID": activity_id,
                "活动日期范围": event_date_range,
                "活动标签": aria_label,
                "活动状态": date_status,
                "活动描述": activity_description,
                "活动链接": activity_link
            }
            
            # 将字典添加到列表中
            activities_info.append(activity_info)

        # 将列表转换为JSON格式并输出
        json_output = json.dumps(activities_info, ensure_ascii=False, indent=4)
        print(json_output)

        # 保存到文件
        with open('output.json', 'w', encoding='utf-8') as f:
            f.write(json_output)

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    target_url = "https://www.macaotourism.gov.mo/zh-hans/events/whatson/"
    crawl_hengqin_activities(target_url)