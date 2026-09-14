from flask import Flask
from flask import render_template
from flask import request
import random

from data.bazi_engine import *
from data.colors import *
from data.themes import *

app = Flask(__name__)

# 🌟 豐富的五行開運宜忌資料庫
ELEMENT_GOOD = {
    "木": [
        "規劃長期願景與藍圖", 
        "進行學習進修與閱讀", 
        "接觸大自然與戶外散步", 
        "發展新興趣與植栽園藝",
        "與貴人朋友交流聚會"
    ],
    "火": [
        "積極展現個人才華", 
        "推動新專案與公開發表", 
        "熱情溝通、拓展人脈", 
        "進行有氧運動提升活力",
        "舉辦慶祝或社交聚會"
    ],
    "土": [
        "穩健理財與資產配置", 
        "徹底整理居家與辦公環境", 
        "建立並落實健康新習慣", 
        "擬定嚴謹合約與計畫",
        "沉澱心靈、腳踏實地"
    ],
    "金": [
        "理性數據分析與覆盤", 
        "精簡開支、評估預算", 
        "執行物品與人際的斷捨離", 
        "做出果斷且專業的決策",
        "專注細節、精益求精"
    ],
    "水": [
        "深度思考與靈感創作", 
        "靜心冥想、調整內在情緒", 
        "閱讀歷史或哲學反思", 
        "溫和傾聽他人需求",
        "靈活應對各種突發變化"
    ]
}

ELEMENT_BAD = {
    "木": [
        "過度僵化、拒絕改變", 
        "猶豫不決而錯失良機", 
        "作息不規律、熬夜傷身", 
        "無謂的鑽牛角尖",
        "給自己過大精神壓力"
    ],
    "火": [
        "衝動發脾氣或情緒失控", 
        "盲目冒險、過度投機", 
        "急於求成而忽略細節", 
        "過度消耗精力導致疲憊",
        "與人起不必要的爭執"
    ],
    "土": [
        "固執己見、聽不進建言", 
        "思慮過多而陷入內耗", 
        "拖延怠惰、抗拒行動", 
        "過度封閉自我",
        "因循守舊、缺乏突破"
    ],
    "金": [
        "過度挑剔、對人嚴苛", 
        "冷酷爭執、缺乏同理心", 
        "因過度緊繃而導致焦慮", 
        "固步自封、不願妥協",
        "過度計較小失誤"
    ],
    "水": [
        "想太多導致悲觀情緒", 
        "逃避現實與應面對的問題", 
        "情緒化決策、隨波逐流", 
        "夜間思緒過多而失眠",
        "過度感性而失去理性判斷"
    ]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    year = int(request.form["year"])
    month = int(request.form["month"])
    day = int(request.form["day"])

    bazi = get_bazi(year, month, day)
    day_master = get_day_master(bazi["day"])
    elements = get_elements(bazi)
    useful_element = get_useful_element(elements)
    theme = get_theme(useful_element)
    lucky_colors = LUCKY_COLORS[useful_element]

    # 🌟 處理四柱文字與日主的五行彩色標籤
    def colorize_pillar(pillar_str):
        if not pillar_str:
            return ""
        res = ""
        for char in pillar_str:
            color = get_char_color(char)
            res += f'<span style="color: {color}; font-weight: bold; text-shadow: 0 0 8px {color}66;">{char}</span>'
        return res

    colored_bazi = {
        "year": colorize_pillar(bazi["year"]),
        "month": colorize_pillar(bazi["month"]),
        "day": colorize_pillar(bazi["day"]),
        "hour": colorize_pillar(bazi["hour"])
    }

    colored_day_master = colorize_pillar(day_master)

    # 🌟 隨機從該五行抽樣 3 個宜忌項目
    good_list = random.sample(ELEMENT_GOOD.get(useful_element, ELEMENT_GOOD["木"]), 3)
    bad_list = random.sample(ELEMENT_BAD.get(useful_element, ELEMENT_BAD["木"]), 3)

    return render_template(
        "result.html",
        bazi=colored_bazi,
        day_master=colored_day_master,
        theme=theme,
        lucky_colors=lucky_colors,
        good=good_list,
        bad=bad_list
    )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)