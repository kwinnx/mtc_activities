from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

"""

"""

def crawl_event_details(url):
    try:
        # 设置Chrome选项
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")  # 无头模式

        # 初始化Chrome WebDriver
        service = Service(executable_path='C:\\Users\\user\\chromedriver\\chromedriver.exe')  # 替换为您的chromedriver路径
        driver = webdriver.Chrome(service=service, options=options)

        # 打开网页
        driver.get(url)
        print(f"当前页面URL: {driver.current_url}")  # 打印当前页面的URL

        # 等待页面加载完成
        wait = WebDriverWait(driver, 20)  # 增加等待时间
        element = (By.CLASS_NAME, 'app-list__notices')  # 等待通知列表加载完成
        print(f"等待元素: {element}")  # 打印等待的元素
        wait.until(EC.presence_of_element_located(element))
        print("页面加载完成")  # 打印页面加载完成的提示

        # 获取页面内容
        page_content = driver.page_source
        print(f"页面内容长度: {len(page_content)}")  # 打印页面内容的长度

        # 关闭浏览器
        driver.quit()

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(page_content, 'html.parser')
        print(f"解析后的HTML内容: {soup.prettify()}")  # 打印解析后的HTML内容

        # 查找所有通知项
        notices = soup.find_all('li')  # 根据实际结构调整选择器
        print(f"找到的通知项数量: {len(notices)}")  # 打印找到的通知项数量
        notice_details_list = []

        for notice in notices:
            # 提取时间
            time_div = notice.find('div', class_='time')
            if not time_div:
                continue  # 如果没有时间，跳过该通知项

            day = time_div.find('strong').text.strip()
            month = time_div.find('span').text.strip()
            year = time_div.find_all('span')[1].text.strip()
            time_text = f"{day} {month} {year}"

            # 提取活动链接和标题
            title_link = notice.find('a', class_='title')
            if not title_link:
                continue  # 如果没有标题链接，跳过该通知项

            title = title_link.text.strip()
            link_href = title_link.get('href')

            # 将提取的信息存储为一个字典，并添加到列表中
            notice_details_list.append({
                "时间": time_text,
                "活动链接": link_href,
                "活动标题": title
            })

        return notice_details_list
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    url = "https://www.hengqin.gov.cn/macao_zh_hans/hzqgl/dtyw/index.html "
    events = crawl_event_details(url)

    # 打印提取的信息
    for event in events:
        print(event)

    # 保存到文件
    with open('shendu.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=4) 