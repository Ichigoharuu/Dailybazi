from lunar_python import Solar, Lunar
from collections import Counter
from datetime import datetime

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

# 地支藏干表與力量分配（地支主氣、中氣、餘氣）
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

# 六沖對照表
CLASH_MAP = {
    "子": "午", "午": "子", "丑": "未", "未": "丑",
    "寅": "申", "申": "寅", "卯": "酉", "酉": "卯",
    "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳"
}

DAY_MASTER_PROFILES = {
    "甲": {"nature": "棟樑之木", "traits": "仁慈正直、具有領袖氣質與開拓精神，如參天大樹立於天地。"},
    "乙": {"nature": "花草之木", "traits": "身段柔韌、適應力極強，善於借力使力、以柔克剛。"},
    "丙": {"nature": "太陽之火", "traits": "熱情坦率、光芒四射，具強大感染力，行事果敢需防急躁。"},
    "丁": {"nature": "燭光之火", "traits": "溫和內斂、洞察敏銳，思維深邃且具備強烈的奉獻精神。"},
    "戊": {"nature": "城牆之土", "traits": "厚重沉穩、誠信包容，如大地山嶽般穩健可靠。"},
    "己": {"nature": "田園之土", "traits": "溫婉包容、多才多藝，心思細膩，善於涵養滋潤他人。"},
    "庚": {"nature": "斧鉞之金", "traits": "剛毅果決、講義氣且崇尚效率，破局能力極強。"},
    "辛": {"nature": "珠寶之金", "traits": "精緻溫潤、自尊心強，具備極佳的審美與對細節的敏銳度。"},
    "壬": {"nature": "江河之水", "traits": "奔湧豪邁、機智通達，具宏觀眼界與強大的應變力。"},
    "癸": {"nature": "雨露之水", "traits": "平靜靈動、直覺敏銳，潤物細無聲，內心情感豐富深邃。"}
}

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
    """取得當日流日與流時干支"""
    now = datetime.now()
    solar = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, 0, 0)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()
    return {
        "day_ganzhi": ec.getDay(),
        "day_branch": ec.getDay()[1]
    }

def calculate_daily_relation(user_day_branch, today_branch):
    """計算命主日支與今日流日的生剋合沖"""
    if CLASH_MAP.get(user_day_branch) == today_branch:
        return f"今日逢「{user_day_branch}{today_branch}相沖」氣場，能量波動較大，宜謹言慎行，避免做衝動決定。"
    elif user_day_branch == today_branch:
        return f"今日逢「{today_branch}字同行」，心緒敏銳，適合專注個人事務、沉澱內在。"
    else:
        return "今日流日氣場平順，陰陽流轉適宜，適合穩步推進計畫。"

def get_elements_percentage(bazi):
    """計算權重五行（天干各1分，月令地支加權3分，其他地支加權1.5分，並含藏干）"""
    scores = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}
    
    pillars = [
        (bazi["year"][0], bazi["year"][1], 1.0, 1.2),
        (bazi["month"][0], bazi["month"][1], 1.2, 3.0), # 月令權重最高
        (bazi["day"][0], bazi["day"][1], 1.2, 1.5),
        (bazi["hour"][0], bazi["hour"][1], 1.0, 1.2)
    ]

    for stem, branch, stem_w, branch_w in pillars:
        # 天干分數
        scores[STEM_ELEMENT[stem]] += stem_w
        # 地支藏干加權
        for hidden_stem, ratio in BRANCH_HIDDEN[branch]:
            elem = STEM_ELEMENT[hidden_stem]
            scores[elem] += branch_w * ratio

    total = sum(scores.values())
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