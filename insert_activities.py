import json
import pymysql
import datetime
import time
import re
import config

# 数据库连接配置
db = pymysql.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME,
    charset=config.DB_CHARSET,
    cursorclass=config.DB_CURSORCLASS
)

# 自增函数，从3开始
def auto_increment_id(start=3):
    current_id = start
    while True:
        yield current_id
        current_id += 1


cursor = db.cursor()

def get_first_image_url(detail_imgs):
    # 遍历detail_imgs列表，提取第一个包含的有效URL
    for img_str in detail_imgs:
        # 使用正则表达式从字符串中提取URL
        match = re.search(r'http[s]?://[^\s<>"]+', img_str)
        if match:
            return match.group(0)  
    return ""  # 如果没有找到有效的URL，则返回空字符串

# 转化时间戳
def str_to_timestamp(time_str):
    dt = datetime.strptime(time_str, "%Y年%m月%d日（%A）%H:%M-%H:%M")
    return int(time.mktime(dt.timetuple()))

# 加载JSON数据
with open('processed_minsheng.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建自增ID生成器
id_generator = auto_increment_id(start=3)


def parse_date(date_str):
    """解析日期字符串，返回 datetime.date 对象"""
    for fmt in ("%Y年%m月%d日", "%Y-%m-%d", "%B %d日"):
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass

    # 处理 "2023年8月19日（星期六）16:00至222:30" 这种格式
    if "至" in date_str:
        start_str, end_str = date_str.split("至")
        start_date = datetime.datetime.strptime(start_str.strip(), "%Y年%m月%d日(%w天)%H:%M").date()
        end_time = datetime.datetime.strptime(end_str.strip(), "%H:%M").time()
        end_date = start_date + datetime.timedelta(days=1)
        return start_date, end_date.replace(hour=0, minute=0, second=0)
    # 处理 "10月3日晚" 这种格式
    match = re.match(r"(\d+)月(\d+)日晚", date_str)
    if match:
        return datetime.datetime.strptime(f"{match.group(1)}月{match.group(2)}日", "%m月%d日").date(), datetime.datetime.strptime(f"{match.group(1)}月{match.group(2)}日", "%m月%d日").date() + datetime.timedelta(days=1)
    return None

def parse_date_range(date_str):
    """解析日期范围字符串，返回 (start_date, end_date)"""
    if "至" in date_str:
        start_date_str, end_date_str = date_str.split("至")
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        return start_date, end_date
    elif "、" in date_str:
        dates = [parse_date(d + "日") for d in date_str.split("、")]
        return dates[0][0], dates[-1][1]
    elif "晚" in date_str:
        month_day = re.search(r"(\d+)月(\d+)日", date_str).groups()
        return parse_date(f"{month_day[0]}月{month_day[1]}日")[0], parse_date(f"{month_day[0]}月{month_day[1]}日")[1]
    elif "开展" in date_str and "持续到" in date_str:
        start_date_str = re.search(r"(\d+月\d+号)开展", date_str).group(1)
        end_date_str = re.search(r"持续到(\d+月\d+日)", date_str).group(1)
        return parse_date(start_date_str)[0], parse_date(end_date_str)[1]
    else:
        return parse_date(date_str), parse_date(date_str)

def convert_to_timestamp(date_obj):
    """将 datetime.date 对象转换为 Unix 时间戳"""
    if date_obj is None:
        return 0
    return int(time.mktime(date_obj.timetuple()))

def process_date(structured_info):
    """处理 structured_info 中的时间字段"""
    time_str = structured_info.get("时间", "")
    start_date, end_date = parse_date_range(time_str)
    start_date_timestamp = convert_to_timestamp(start_date) if start_date is not None else 0
    end_date_timestamp = convert_to_timestamp(end_date) + 86399 if end_date is not None else 0  # 添加 23 小时 59 分 59 秒
    structured_info["start_date"] = start_date_timestamp
    structured_info["end_date"] = end_date_timestamp

for item in data:
    title = item.get("标题", "").strip()
    if not title:
        title = item.get("structured_info", {}).get("活动主题", "").strip()
    info = item.get("structured_info", {})
    description = item.get("original_content", "").strip()
    lng = float(info.get("经度", 0))
    lat = float(info.get("纬度", 0))
    #print(info.get("地点", ""))
    location = info.get("地点", "").strip()
    #location = info.get("地点", [""])[0].strip() if info.get("地点") else ""

    ###待办class = info.get("class","")

    poster_url = item.get("图片链接", "")
    if not poster_url:
        poster_url = get_first_image_url(item.get("detail_imgs", []))

    print(poster_url)


    org_name = item.get("structured_info", {}).get("主办方", "").strip()



    time_str = info.get("时间", "").replace("（周", "（")
    schedule_title = item.get("structured_info", {}).get("活动主题", "").strip()
    #print(item.get("structured_info", {}).get("活动内容", ""))
    schedule_content = item.get("structured_info", {}).get("活动内容", "").strip()

    process_date(info)
    #print(info["start_date"], info["end_date"])

    now = int(time.time())

    products = "[]"

    if poster_url is None or title is None or title.strip() == "" or poster_url.strip() == "":
        print("Skipping this record because poster_url or title is empty.")
    else:
        id = next(id_generator)
    # 插入主表
        insert_sql = """
            INSERT INTO sxo_plugins_activities
            (id, name, start_date, end_date, location, lng, lat, description, products, poster_url, status, add_time, upd_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, 0, %s, %s)
        """
        cursor.execute(insert_sql, (
            id, title, info["start_date"], info["end_date"], location, lng, lat,
            description, products, poster_url, now, now
        ))


        # 插入组织架构表 (主办方、合办方、赞助方)

        org_type = item.get("type", 0)  # 默认为0：主办方
        org_region = item.get("region", "广东").strip()
        org_logo_url = item.get("logo_url", "").strip()

        # 插入组织信息
        insert_org_sql = """
            INSERT INTO sxo_plugins_activity_organizations
            ( activity_id, name, type, region, logo_url, add_time, upd_time)
            VALUES ( %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_org_sql, (
            id, org_name, org_type, org_region, org_logo_url, now, now
        ))

        # 插入活动日程表
        schedule_type =  0  
        max_capacity = 0

        # 插入日程信息
        insert_schedule_sql = """
            INSERT INTO sxo_plugins_activity_schedules
            (activity_id, schedule_date, title, content, type, max_capacity, add_time, upd_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
            
        cursor.execute(insert_schedule_sql, (
            id, time_str, schedule_title, schedule_content, schedule_type, max_capacity, now, now
        ))

        #插入活动类型join表  待办




db.commit()
cursor.close()
db.close()
print("数据插入完毕")
