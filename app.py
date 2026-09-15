import os
from flask import Flask, render_template, request, jsonify

from data.bazi_engine import (
    get_bazi,
    STEM_ELEMENT,
    DAY_MASTER_PROFILES,
    get_elements_percentage,
    get_useful_element,
    get_today_stream,
    calculate_daily_relation,
    get_hourly_energy
)
from data.colors import get_char_color, LUCKY_COLORS
from data.themes import get_theme
from data.ai_master import get_ai_fortune, consult_ai_master

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

    raw_bazi = get_bazi(year, month, day, hour)
    day_stem = raw_bazi["day"][0]
    day_branch = raw_bazi["day"][1]
    day_elem = STEM_ELEMENT[day_stem]
    day_profile = DAY_MASTER_PROFILES.get(day_stem, {})

    elements_scores, elements_distribution = get_elements_percentage(raw_bazi)
    useful_element = get_useful_element(elements_scores)
    theme = get_theme(useful_element)
    lucky_colors = LUCKY_COLORS[useful_element]

    today_stream = get_today_stream()
    stream_notice = calculate_daily_relation(day_branch, today_stream["day_branch"])
    hourly_energy = get_hourly_energy(day_branch, useful_element)

    ai_fortune = get_ai_fortune(
        bazi=raw_bazi,
        day_master=f"{day_stem}{day_elem}",
        day_profile=day_profile,
        distribution=elements_distribution,
        useful_element=useful_element,
        focus_topic=focus_topic
    )

    good_list = ai_fortune.get("good", ["專注手頭事務", "適時深呼吸", "早點休息"])
    bad_list = ai_fortune.get("bad", ["盲目跟風焦慮", "衝動發脾氣", "過度內耗拖延"])

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
        "hour": colorize_pillar(raw_bazi["hour"])
    }

    bazi_summary_str = (
        f"四柱:[{raw_bazi['year']} {raw_bazi['month']} {raw_bazi['day']} {raw_bazi['hour']}], "
        f"日主:{day_stem}{day_elem}, 喜用神:{useful_element}, 關注重心:{focus_topic}"
    )

    return render_template(
        "result.html",
        bazi=colored_bazi,
        raw_summary=bazi_summary_str,
        day_master=f"{colorize_pillar(day_stem)}（{colorize_pillar(day_elem)}）",
        day_profile=day_profile,
        distribution=elements_distribution,
        useful_element=useful_element,
        ai_fortune=ai_fortune,
        focus_topic=focus_topic,
        today_stream=today_stream,
        stream_notice=stream_notice,
        hourly_energy=hourly_energy,
        theme=theme,
        lucky_colors=lucky_colors,
        good=good_list,
        bad=bad_list
    )

@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.get_json() or {}
    bazi_summary = data.get("summary", "")
    question = data.get("question", "")
    if not question.strip():
        return jsonify({"reply": "請輸入你想向大師請教的具體問題。"})
    reply = consult_ai_master(bazi_summary, question)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)