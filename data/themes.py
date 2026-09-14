import random

THEMES = {
    "木":[
        {"title":"🌱 新芽萌發", "desc":"今天適合播下新的種子，專注於未來成長。", "color":"#0F3D2E"},
        {"title":"🌿 靜水生長", "desc":"慢一點沒有關係，重要的是持續前進。", "color":"#14532D"}
    ],
    "火":[
        {"title":"🔥 行動之火", "desc":"是時候採取行動，不要停留在想法階段。", "color":"#7A1E1E"},
        {"title":"☀️ 光芒綻放", "desc":"今天適合展現自己。", "color":"#A83232"}
    ],
    "土":[
        {"title":"🏔 穩固根基", "desc":"打穩基礎比追求速度更重要。", "color":"#7C5A2E"},
        {"title":"🌾 厚土豐收", "desc":"過去累積的成果正在慢慢顯現。", "color":"#B08D57"}
    ],
    "金":[
        {"title":"💎 金色契機", "desc":"今天容易出現值得把握的機會。", "color":"#D4AF37"},
        {"title":"⚖️ 平衡天秤", "desc":"理性分析將帶來更好的決定。", "color":"#C5A028"}
    ],
    "水":[
        {"title":"⭐ 星辰導航", "desc":"重新校準方向，未來將更清晰。", "color":"#0D1B2A"},
        {"title":"🌙 月影沉思", "desc":"今天適合反思與自我提升。", "color":"#1B263B"}
    ]
}

def get_theme(element):
    return random.choice(THEMES[element])