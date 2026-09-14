from lunar_python import Solar
from collections import Counter

STEM_ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

BRANCH_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

def get_bazi(year, month, day):
    solar = Solar.fromYmdHms(year, month, day, 12, 0, 0)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()

    return {
        "year": ec.getYear(),
        "month": ec.getMonth(),
        "day": ec.getDay(),
        "hour": ec.getTime()
    }

def get_day_master(day_pillar):
    stem = day_pillar[0]
    return stem + STEM_ELEMENT[stem]

def get_elements(bazi):
    elements = []
    for pillar in bazi.values():
        stem = pillar[0]
        branch = pillar[1]
        elements.append(STEM_ELEMENT[stem])
        elements.append(BRANCH_ELEMENT[branch])

    counter = Counter(elements)
    for e in ["木", "火", "土", "金", "水"]:
        if e not in counter:
            counter[e] = 0
    return counter

def get_useful_element(counter):
    return min(counter, key=counter.get)