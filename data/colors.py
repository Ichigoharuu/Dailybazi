# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:53:36 2026

@author: user
"""
LUCKY_COLORS = {
    "木": ["墨綠色", "翡翠綠"],
    "火": ["酒紅色", "暖橙色"],
    "土": ["米金色", "咖啡色"],
    "金": ["象牙白", "鎏金色"],
    "水": ["深海藍", "曜石黑"]
}

# 🌟 天干地支專屬字體五行色
ELEMENT_COLORS = {
    "木": "#2ECC71",  # 翠綠色
    "火": "#E74C3C",  # 烈紅色
    "土": "#D4AC0D",  # 琥珀金
    "金": "#F4D03F",  # 鎏金黃
    "水": "#3498DB"   # 深海藍
}

STEM_ELEMENT = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

BRANCH_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

def get_char_color(char):
    if char in STEM_ELEMENT:
        return ELEMENT_COLORS[STEM_ELEMENT[char]]
    elif char in BRANCH_ELEMENT:
        return ELEMENT_COLORS[BRANCH_ELEMENT[char]]
    return "#EAEAEA"