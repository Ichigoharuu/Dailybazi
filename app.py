import os
from flask import Flask, render_template, request

from data.bazi_engine import (
    get_bazi,
    STEM_ELEMENT,
    DAY_MASTER_PROFILES,
    get_elements_percentage,
    get_useful_element,
    get_today_stream,
    calculate_daily_relation,
)
from data.colors import get_char_color, LUCKY_COLORS
from data.themes import get_theme
from data.ai_master import get_ai_fortune

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    year = int(request.form["year"])
    month = int(request.form["month"])
    day = int(request.form["day"])
    hour = int(request.form.get("hour", 12))
    focus_topic = request.form.get("focus_topic", "事業發展與決策突破")

    # 1. 取得原局八字與日主
    raw_bazi = get_bazi(year, month, day, hour)
    day_stem = raw_bazi["day"][0]
    day_branch = raw_bazi["day"][1]
    day_elem = STEM_ELEMENT[day_stem]
    day_profile = DAY_MASTER_PROFILES.get(day_stem, {})

    # 2. 地支藏干加權計算與喜用神
    elements_scores, elements_distribution = get_elements_percentage(raw_bazi)
    useful_element = get_useful_element(elements_scores)
    theme = get_theme(useful_element)
    lucky_colors = LUCKY_COLORS[useful_element]

    # 3. 今日動態流日與生剋提示
    today_stream = get_today_stream()
    stream_notice = calculate_daily_relation(day_branch, today_stream["day_branch"])

    # 4. LLM 全方位生成（白話分析、客製宜忌、開運飲食、金句）
    ai_fortune = get_ai_fortune(
        bazi=raw_bazi,
        day_master=f"{day_stem}{day_elem}",
        day_profile=day_profile,
        distribution=elements_distribution,
        useful_element=useful_element,
        focus_topic=focus_topic,
    )

    good_list = ai_fortune.get("good", ["專注手頭事務", "適時深呼吸", "早點休息"])
    bad_list = ai_fortune.get("bad", ["盲目跟風焦慮", "衝動發脾氣", "過度內耗拖延"])

    # 5. 八字霓虹文字上色
    def colorize_pillar(pillar_str):
        if not pillar_str:
            return ""
        res = ""
        for char in pillar_str:
            color = get_char_color(char)
            res += f'<span style="color: {color}; font-weight: bold; text-shadow: 0 0 8px {color}66;">{char}</span>'
        return res

    colored_bazi = {
        "year": colorize_pillar(raw_bazi["year"]),
        "month": colorize_pillar(raw_bazi["month"]),
        "day": colorize_pillar(raw_bazi["day"]),
        "hour": colorize_pillar(raw_bazi["hour"]),
    }

    colored_day_master = f"{colorize_pillar(day_stem)}（{colorize_pillar(day_elem)}）"

    return render_template(
        "result.html",
        bazi=colored_bazi,
        day_master=colored_day_master,
        day_profile=day_profile,
        distribution=elements_distribution,
        useful_element=useful_element,
        ai_fortune=ai_fortune,
        focus_topic=focus_topic,
        today_stream=today_stream,
        stream_notice=stream_notice,
        theme=theme,
        lucky_colors=lucky_colors,
        good=good_list,
        bad=bad_list,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)