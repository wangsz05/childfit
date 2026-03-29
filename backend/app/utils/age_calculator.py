"""
年龄计算工具
"""
from datetime import date
from typing import Tuple


def calculate_age(birth_date: date, reference_date: date = None) -> int:
    """
    计算年龄
    
    Args:
        birth_date: 出生日期
        reference_date: 参考日期 (默认今天)
        
    Returns:
        年龄 (岁)
    """
    if reference_date is None:
        reference_date = date.today()
    
    years = reference_date.year - birth_date.year
    
    # 如果还没过生日，减 1 岁
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        years -= 1
    
    return max(0, years)


def get_age_group(age: int) -> str:
    """
    获取年龄段分组
    
    Args:
        age: 年龄
        
    Returns:
        年龄段标识
    """
    if age < 3:
        return "toddler"  # 婴幼儿
    elif age < 6:
        return "preschool"  # 学龄前
    elif age < 12:
        return "primary"  # 小学
    elif age < 15:
        return "middle"  # 初中
    elif age < 18:
        return "high"  # 高中
    else:
        return "adult"  # 成人


def get_age_group_name(age_group: str) -> str:
    """
    获取年龄段中文名称
    
    Args:
        age_group: 年龄段标识
        
    Returns:
        中文名称
    """
    age_group_names = {
        "toddler": "婴幼儿 (0-2 岁)",
        "preschool": "学龄前 (3-5 岁)",
        "primary": "小学 (6-11 岁)",
        "middle": "初中 (12-14 岁)",
        "high": "高中 (15-17 岁)",
        "adult": "成人 (18 岁+)",
    }
    return age_group_names.get(age_group, "未知")


def is_age_appropriate(age: int, age_min: int, age_max: int) -> bool:
    """
    判断年龄是否在指定范围内
    
    Args:
        age: 当前年龄
        age_min: 最小年龄
        age_max: 最大年龄
        
    Returns:
        是否适合
    """
    return age_min <= age <= age_max


def calculate_age_and_group(birth_date: date) -> Tuple[int, str, str]:
    """
    计算年龄和年龄段
    
    Args:
        birth_date: 出生日期
        
    Returns:
        (年龄，年龄段标识，年龄段名称)
    """
    age = calculate_age(birth_date)
    age_group = get_age_group(age)
    age_group_name = get_age_group_name(age_group)
    
    return age, age_group, age_group_name
