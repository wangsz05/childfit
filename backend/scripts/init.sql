-- ChildFit 数据库初始化脚本
-- MySQL 8.0+

-- 创建数据库 (如果不存在)
CREATE DATABASE IF NOT EXISTS childfit DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE childfit;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    wx_openid VARCHAR(64) UNIQUE NOT NULL COMMENT '微信 OpenID',
    phone VARCHAR(20) COMMENT '手机号',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar_url VARCHAR(255) COMMENT '头像',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_wx_openid (wx_openid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 孩子档案表
CREATE TABLE IF NOT EXISTS child_profiles (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL COMMENT '所属用户 ID',
    name VARCHAR(50) NOT NULL COMMENT '孩子姓名',
    birth_date DATE NOT NULL COMMENT '出生日期',
    gender ENUM('male', 'female') NOT NULL COMMENT '性别',
    height DECIMAL(5,2) COMMENT '身高 (cm)',
    weight DECIMAL(5,2) COMMENT '体重 (kg)',
    city VARCHAR(50) COMMENT '城市',
    family_structure ENUM('two_parent', 'single_parent', 'left_behind', 'other') COMMENT '家庭结构',
    economic_status ENUM('low', 'medium', 'high') COMMENT '经济状况',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_birth_date (birth_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='孩子档案表';

-- 活动库表
CREATE TABLE IF NOT EXISTS activities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '活动名称',
    description TEXT COMMENT '活动描述',
    age_min INT NOT NULL COMMENT '最小年龄',
    age_max INT NOT NULL COMMENT '最大年龄',
    type ENUM('indoor', 'outdoor', 'any') NOT NULL COMMENT '活动类型',
    cost_level ENUM('free', 'low', 'medium', 'high') NOT NULL COMMENT '成本等级',
    duration_min INT COMMENT '推荐时长 (分钟)',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_age_range (age_min, age_max),
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='活动库表';

-- 插入示例活动数据
INSERT INTO activities (id, name, description, age_min, age_max, type, cost_level, duration_min, status) VALUES
('act_001', '跳绳', '基础跳绳运动，锻炼心肺功能', 6, 18, 'outdoor', 'free', 20, 'active'),
('act_002', '室内瑜伽', '适合雨天的室内拉伸运动', 8, 18, 'indoor', 'free', 30, 'active'),
('act_003', '亲子跑步', '家长陪同的户外跑步活动', 5, 18, 'outdoor', 'free', 30, 'active'),
('act_004', '眼保健操', '保护视力的眼部按摩操', 3, 18, 'any', 'free', 5, 'active'),
('act_005', '篮球', '户外篮球运动', 10, 18, 'outdoor', 'low', 60, 'active');

-- 每日计划表
CREATE TABLE IF NOT EXISTS daily_plans (
    id VARCHAR(36) PRIMARY KEY,
    child_id VARCHAR(36) NOT NULL COMMENT '孩子 ID',
    plan_date DATE NOT NULL COMMENT '计划日期',
    weather_snapshot JSON COMMENT '天气快照',
    plan_data JSON NOT NULL COMMENT '计划内容',
    status ENUM('generated', 'confirmed', 'completed', 'skipped') DEFAULT 'generated' COMMENT '状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES child_profiles(id) ON DELETE CASCADE,
    UNIQUE KEY uk_child_date (child_id, plan_date),
    INDEX idx_plan_date (plan_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日计划表';

-- 打卡记录表
CREATE TABLE IF NOT EXISTS check_ins (
    id VARCHAR(36) PRIMARY KEY,
    plan_id VARCHAR(36) NOT NULL COMMENT '计划 ID',
    activity_id VARCHAR(36) COMMENT '活动 ID',
    check_in_type ENUM('manual', 'photo', 'video', 'voice') NOT NULL COMMENT '打卡类型',
    media_url VARCHAR(255) COMMENT '媒体文件 URL',
    duration_min INT COMMENT '实际时长 (分钟)',
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '完成时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES daily_plans(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE SET NULL,
    INDEX idx_plan_id (plan_id),
    INDEX idx_completed_at (completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='打卡记录表';

-- 成就表
CREATE TABLE IF NOT EXISTS achievements (
    id VARCHAR(36) PRIMARY KEY,
    child_id VARCHAR(36) NOT NULL COMMENT '孩子 ID',
    achievement_type VARCHAR(50) NOT NULL COMMENT '成就类型',
    achievement_name VARCHAR(100) NOT NULL COMMENT '成就名称',
    description TEXT COMMENT '成就描述',
    icon_url VARCHAR(255) COMMENT '图标 URL',
    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '获得时间',
    metadata JSON COMMENT '元数据',
    FOREIGN KEY (child_id) REFERENCES child_profiles(id) ON DELETE CASCADE,
    INDEX idx_child_id (child_id),
    INDEX idx_achievement_type (achievement_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成就表';
