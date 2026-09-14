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

DAY_MASTER_PROFILES = {
    "甲": {"nature": "棟樑之木", "traits": "仁慈正直、有上進心，如參天大樹般具領袖氣質，但過硬則易折。"},
    "乙": {"nature": "花草之木", "traits": "身段柔韌、適應力極強，善於借力使力與人際周旋，內心堅韌。"},
    "丙": {"nature": "太陽之火", "traits": "熱情奔放、光明磊落，具感染力與奉獻精神，行事需防急躁衝動。"},
    "丁": {"nature": "燭光之火", "traits": "溫和細膩、洞察敏銳，富有奉獻精神與思想深度，思慮較為深沉。"},
    "戊": {"nature": "城牆之土", "traits": "沉穩厚重、包容力強，誠信可靠且極具定力，偶爾顯得保守頑固。"},
    "己": {"nature": "田園之土", "traits": "溫柔包容、善解人意，具備涵養與多才多藝的特質，容易思慮過多。"},
    "庚": {"nature": "斧鉞之金", "traits": "剛毅果決、講義氣且重效率，善於破局開拓，說話直率需防傷人。"},
    "辛": {"nature": "珠寶之金", "traits": "精緻溫潤、自尊心強，追求完美且注重美感與品味，對細節極其敏感。"},
    "壬": {"nature": "江河之水", "traits": "奔湧豪放、機智靈動，思維開闊且具宏觀視野，需防任性隨心。"},
    "癸": {"nature": "雨露之水", "traits": "平靜內斂、直覺敏銳，善於默默滋養萬物，情感豐富且帶有神祕感。"}
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

def get_day_master(day_pillar):
    stem = day_pillar[0]
    return stem, STEM_ELEMENT[stem]

def get_elements_percentage(bazi):
    elements = []
    for pillar in bazi.values():
        stem = pillar[0]
        branch = pillar[1]
        elements.append(STEM_ELEMENT[stem])
        elements.append(BRANCH_ELEMENT[branch])

    counter = Counter(elements)
    total = len(elements)
    
    distribution = []
    for elem in ["木", "火", "土", "金", "水"]:
        count = counter.get(elem, 0)
        percent = int((count / total) * 100)
        distribution.append({
            "name": elem,
            "count": count,
            "percent": percent
        })
    return counter, distribution

def get_useful_element(counter):
    return min(["木", "火", "土", "金", "水"], key=lambda e: counter.get(e, 0))