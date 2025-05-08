
# 小程序爬虫项目

这是一个用于爬取多个页面数据、处理数据并存储到 MySQL 数据库的小程序爬虫项目。

## 目录结构
project/
│
├── README.md
│
├── requirements.txt        # Python 依赖包列表
│
├──爬虫/
│   ├── re0.py
│   ├── re1.py
│   └── re2.py
│
├── 数据处理/
│   ├── processContent.py   # 数据处理逻辑 提取原文中 时间地点主题主办方 接入讯飞大模型sparkAPI
│   ├── locationprocess.py   #数据处理逻辑 提取爬取的位置 接入高德地理位置编码API 转换为经纬度信息
│   └── duplicate.py    #数据去重处理
│
├── 数据库/
│   ├── install.sql   # 数据库表创建脚本
│   └── insert_data.py     # 数据插入 MySQL 脚本
│
└── output/                 # 存放输出文件
    ├── activities_detail.json          # 爬取的数据存储为 JSON 格式
    ├── processed_activities.json          # 爬取的数据存储为 JSON 格式
    ├── structured_activities.json          # 爬取的数据存储为 JSON 格式
    ├── wenhua.json          # 爬取的数据存储为 JSON 格式
    ├── wenhua_test.json          # 爬取的数据存储为 JSON 格式
    └── processed_minsheng.json    
