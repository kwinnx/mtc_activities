# 活动主表
CREATE TABLE IF NOT EXISTS `{PREFIX}plugins_activities` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `name` VARCHAR(100) NOT NULL COMMENT '活动名称',
  `start_date` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '开始日期',
  `end_date` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '结束日期',
  `location` VARCHAR(200) NOT NULL COMMENT '活动地点',
  `lng` decimal(13,10) NOT NULL DEFAULT '0.0000000000' COMMENT '经度',
  `lat` decimal(13,10) NOT NULL DEFAULT '0.0000000000' COMMENT '纬度',
  `description` TEXT COMMENT '活动描述',
  `products` TEXT COMMENT '关联商品',
  `poster_url` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '海报URL',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '状态（0:正常, 1:关闭）',
  `add_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '添加时间',
  `upd_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `add_time` (`add_time`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8 ROW_FORMAT = COMPACT COMMENT ='活动主表';

# 组织架构表（存储主办/赞助单位）
CREATE TABLE IF NOT EXISTS `{PREFIX}plugins_activity_organizations` (
   `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
   `activity_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '活动id',
   `name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '组织名称',
   `type` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '组织类型(0:主办方, 1:合办方, 2:赞助方)',
   `region` VARCHAR(50) NOT NULL DEFAULT '' COMMENT '所在地区',
   `logo_url` VARCHAR(200) NOT NULL DEFAULT '' COMMENT 'logo',
   `add_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '添加时间',
   `upd_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
   PRIMARY KEY (`id`),
   KEY `activity_id` (`activity_id`),
   KEY `add_time` (`add_time`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8 ROW_FORMAT = COMPACT COMMENT ='组织架构表（存储主办/赞助单位）';

# 活动日程表
CREATE TABLE IF NOT EXISTS `{PREFIX}plugins_activity_schedules` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `activity_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '活动id',
  `schedule_date` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '日程日期',
  `title` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '日程标题',
  `content` TEXT NOT NULL COMMENT '日程内容',
  `type` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '0:通用, 1:展览, 2:竞赛, 3:演讲',
  `max_capacity` int(11) NOT NULL DEFAULT '0' COMMENT '最大承载人数',
  `add_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '添加时间',
  `upd_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `activity_id` (`activity_id`),
  KEY `add_time` (`add_time`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8 ROW_FORMAT = COMPACT COMMENT ='活动日程表';

# 参展产品表
CREATE TABLE IF NOT EXISTS `{PREFIX}plugins_activity_products` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `activity_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '活动id',
  `product_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '产品id',
  `add_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '添加时间',
  `upd_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `activity_id` (`activity_id`),
  KEY `add_time` (`add_time`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8 ROW_FORMAT = COMPACT COMMENT ='参展产品表';

# 预约记录表
CREATE TABLE IF NOT EXISTS `{PREFIX}plugins_activity_reservations` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `user_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '用户id',
  `activity_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '活动id',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '0:确认, 1:待定, 2:取消',
  `quantity` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '预约人数',
  `add_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '添加时间',
  `upd_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `activity_id` (`activity_id`),
  KEY `add_time` (`add_time`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8 ROW_FORMAT = COMPACT COMMENT ='预约记录表';

# 活动分类
CREATE TABLE IF NOT EXISTS `{PREFIX}plugins_activity_category` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `pid` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '父id',
  `icon` char(255) NOT NULL DEFAULT '' COMMENT 'icon图标',
  `name` char(60) NOT NULL DEFAULT '' COMMENT '名称',
  `vice_name` char(80) NOT NULL DEFAULT '' COMMENT '副标题',
  `describe` char(255) NOT NULL DEFAULT '' COMMENT '描述',
  `bg_color` char(30) NOT NULL DEFAULT '' COMMENT 'css背景色值',
  `big_images` char(255) NOT NULL DEFAULT '' COMMENT '大图片',
  `is_home_recommended` tinyint(2) unsigned NOT NULL DEFAULT '0' COMMENT '是否首页推荐（0否, 1是）',
  `sort` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '排序',
  `is_enable` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否启用（0否，1是）',
  `seo_title` char(100) NOT NULL DEFAULT '' COMMENT 'SEO标题',
  `seo_keywords` char(130) NOT NULL DEFAULT '' COMMENT 'SEO关键字',
  `seo_desc` char(230) NOT NULL DEFAULT '' COMMENT 'SEO描述',
  `add_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '添加时间',
  `upd_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='活动分类';

# 分类关联
CREATE TABLE IF NOT EXISTS `{PREFIX}plugins_activity_category_join` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `activity_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '活动id',
  `category_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '分类id',
  `add_time` int(11) unsigned DEFAULT '0' COMMENT '添加时间',
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `activity_id` (`activity_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='活动分类关联';