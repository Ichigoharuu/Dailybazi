from datetime import datetime
from lunar_python import Solar

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

# 地支藏干與分配比例
BRANCH_HIDDEN = {
    "子": [("癸", 1.0)],
    "丑": [("己", 0.6), ("癸", 0.3), ("辛", 0.1)],
    "寅": [("甲", 0.6), ("丙", 0.3), ("戊", 0.1)],
    "卯": [("乙", 1.0)],
    "辰": [("戊", 0.6), ("乙", 0.3), ("癸", 0.1)],
    "巳": [("丙", 0.6), ("庚", 0.3), ("戊", 0.1)],
    "午": [("丁", 0.7), ("己", 0.3)],
    "未": [("己", 0.6), ("丁", 0.3), ("乙", 0.1)],
    "申": [("庚", 0.6), ("壬", 0.3), ("戊", 0.1)],
    "酉": [("辛", 1.0)],
    "戌": [("戊", 0.6), ("辛", 0.3), ("丁", 0.1)],
    "亥": [("壬", 0.7), ("甲", 0.3)]
}

# 六沖對照
CLASH_MAP = {
    "子": "午", "午": "子", "丑": "未", "未": "丑",
    "寅": "申", "申": "寅", "卯": "酉", "酉": "卯",
    "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳"
}

# 日主性格原型
DAY_MASTER_PROFILES = {
    "甲": {"nature": "棟樑之木", "traits": "正直仁慈、具備大格局與開拓領導力，如參天大樹拔地而起。"},
    "乙": {"nature": "花草柔木", "traits": "柔韌靈活、適應力極強，善於借勢借力、以柔克剛。"},
    "丙": {"nature": "燦爛烈陽", "traits": "坦蕩明亮、熱情果決，極富感染力與號召力，宜防急躁。"},
    "丁": {"nature": "靜夜燭火", "traits": "溫婉內斂、洞察敏銳，思維深邃且具備強烈奉獻精神。"},
    "戊": {"nature": "沉穩厚土", "traits": "厚德載物、誠信穩健，包容度極高，如泰山磐石般可靠。"},
    "己": {"nature": "溫潤田園", "traits": "細膩包容、多才多藝，心思縝密，極善於滋養照拂他人。"},
    "庚": {"nature": "剛毅銳金", "traits": "果斷俐落、重情講義，行動力與執行力極強，崇尚效率。"},
    "辛": {"nature": "溫潤明珠", "traits": "精緻細膩、自尊心強，具有極佳的審美力與敏銳直覺。"},
    "壬": {"nature": "奔湧長江", "traits": "大氣豪爽、智慧如海，具備宏觀思維與極強的應變魄力。"},
    "癸": {"nature": "甘潤晨露", "traits": "寧靜純粹、直覺強烈，潤物無聲，內心世界豐富而敏銳。"}
}

# 十二時辰配置
SHICHEN_LIST = [
    {"name": "子時", "branch": "子", "element": "水", "hours": "23:00-01:00"},
    {"name": "丑時", "branch": "丑", "element": "土", "hours": "01:00-03:00"},
    {"name": "寅時", "branch": "寅", "element": "木", "hours": "03:00-05:00"},
    {"name": "卯時", "branch": "卯", "element": "木", "hours": "05:00-07:00"},
    {"name": "辰時", "branch": "辰", "element": "土", "hours": "07:00-09:00"},
    {"name": "巳時", "branch": "巳", "element": "火", "hours": "09:00-11:00"},
    {"name": "午時", "branch": "午", "element": "火", "hours": "11:00-13:00"},
    {"name": "未時", "branch": "未", "element": "土", "hours": "13:00-15:00"},
    {"name": "申時", "branch": "申", "element": "金", "hours": "15:00-17:00"},
    {"name": "酉時", "branch": "酉", "element": "金", "hours": "17:00-19:00"},
    {"name": "戌時", "branch": "戌", "element": "土", "hours": "19:00-21:00"},
    {"name": "亥時", "branch": "亥", "element": "水", "hours": "21:00-23:00"}
]

def get_bazi(year, month, day, hour=12):
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()
    return {
        "year": ec.getYear(),
        "month": ec.getMonth(),
        "day": ec.getDay(),
        "hour": ec.getTime()
    }

def get_today_stream():
    now = datetime.now()
    solar = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, 0, 0)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()
    return {
        "day_ganzhi": ec.getDay(),
        "day_branch": ec.getDay()[1]
    }

def calculate_daily_relation(user_day_branch, today_branch):
    if CLASH_MAP.get(user_day_branch) == today_branch:
        return f"今日逢「{user_day_branch}{today_branch}相沖」氣場，能量波動較顯著，宜放緩步調，避免衝動做重大決定。"
    elif user_day_branch == today_branch:
        return f"今日逢「{today_branch}字同行」，心緒敏銳，適合專注個人事務、沉澱內在。"
    return "今日流日氣場平順，陰陽流轉適宜，適合穩步推進計畫。"

def get_hourly_energy(user_day_branch, useful_element):
    current_hour = datetime.now().hour
    current_idx = ((current_hour + 1) // 2) % 12
    hourly_data = []
    for idx, item in enumerate(SHICHEN_LIST):
        branch = item["branch"]
        elem = item["element"]
        if elem == useful_element:
            status = "吉 · 能量相生"
            tag = "favorable"
        elif CLASH_MAP.get(user_day_branch) == branch:
            status = "沖 · 宜靜沉澱"
            tag = "clash"
        else:
            status = "平 · 順行推進"
            tag = "neutral"

        hourly_data.append({
            "name": item["name"],
            "hours": item["hours"],
            "element": elem,
            "status": status,
            "tag": tag,
            "is_current": (idx == current_idx)
        })
    return hourly_data

def get_elements_percentage(bazi):
    scores = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}
    pillars = [
        (bazi["year"][0], bazi["year"][1], 1.0, 1.2),
        (bazi["month"][0], bazi["month"][1], 1.2, 3.0),
        (bazi["day"][0], bazi["day"][1], 1.2, 1.5),
        (bazi["hour"][0], bazi["hour"][1], 1.0, 1.2)
    ]
    for stem, branch, stem_w, branch_w in pillars:
        scores[STEM_ELEMENT[stem]] += stem_w
        for hidden_stem, ratio in BRANCH_HIDDEN[branch]:
            elem = STEM_ELEMENT[hidden_stem]
            scores[elem] += branch_w * ratio

    total = sum(scores.values()) or 1.0
    distribution = []
    for elem in ["木", "火", "土", "金", "水"]:
        percent = int(round((scores[elem] / total) * 100))
        distribution.append({
            "name": elem,
            "score": round(scores[elem], 1),
            "percent": percent
        })
    return scores, distribution

def get_useful_element(scores):
    return min(["木", "火", "土", "金", "水"], key=lambda e: scores[e])