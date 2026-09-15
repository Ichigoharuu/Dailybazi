import os
import json
import random
from google import genai
from google.genai import types

RANDOM_PERSPECTIVES = [
    "微風拂面、枝芽初綻之生機",
    "烈火淬金、淬鍊鋒芒之篤定",
    "厚土負載、沉穩蓄力之踏實",
    "秋水長天、沉靜收斂之清朗",
    "清泉繞石、隨順變通之智慧"
]

def get_ai_fortune(bazi, day_master, day_profile, distribution, useful_element, focus_topic="事業發展與決策突破"):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "poem": "平心靜氣迎晨光，順應直覺最心寬。\n不急不躁走己路，好運自然到身邊。",
            "analysis": "目前處於離線沉思模式。今天先別急著做重大決定，放慢腳步深呼吸，專注眼前手頭的事最重要。",
            "good": ["專注完成手頭最重要的一件事", "整理辦公桌面或整理手機相簿", "晚上早半小時上床休息"],
            "bad": ["衝動答應別人的臨時要求", "把時間浪費在無效爭論上", "熬夜滑手機過度內耗"],
            "food_tip": "一杯溫潤的無糖洋甘菊茶",
            "mantra": "別人的節奏是別人的，我走好自己的步調就好。"
        }

    client = genai.Client(api_key=api_key)
    dist_str = ", ".join([f"{item['name']}: {item['percent']}%" for item in distribution])
    perspective = random.choice(RANDOM_PERSPECTIVES)

    prompt = f"""你是一位說話親切、通俗易懂、像好朋友一樣溫暖且有智慧的現代生活命理導師。
請拋棄一切晦澀生硬的術語（嚴格禁止出現「土多金埋」、「日元旺衰」、「比劫剋財」等），轉化為通俗的大白話和生活化比喻。

【命主排盤特質】
- 四柱八字：[{bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}]
- 本命性格：{day_master}（{day_profile.get('nature', '')}），特質：{day_profile.get('traits', '')}
- 先天五行氣場分佈：{dist_str}
- 偏弱需調和元素：{useful_element}
- 當前問命重心：{focus_topic}
- 本次意象引導：{perspective}

請生成以下 6 項內容（語氣務必通俗、現代、溫暖）：
1. poem: 一首四句短詩（每句字數相仿，通俗鼓舞，不要深奧古文）。
2. analysis: 針對「{focus_topic}」的深度白話解盤（120字以內）。用生活比喻點出他目前的狀態，並給出 1~2 個今天就能照著做的心態或行動建議。
3. good: 3 個今天最適合做的白話具體小行動（陣列格式）。
4. bad: 3 個今天最容易踩雷或內耗的行為（陣列格式）。
5. food_tip: 一款符合補充「{useful_element}」能量的日常飲料或餐點。
6. mantra: 一句 15 字以內、能讓人瞬間放下焦慮的心態安撫金句。

請嚴格按照以下 JSON 格式回傳，不得加入額外文字或 markdown 標記：
{{
  "poem": "四句詩（以換行符號 \\n 連接）",
  "analysis": "大白話分析與行動建議",
  "good": ["宜行動一", "宜行動二", "宜行動三"],
  "bad": ["宜避行為一", "宜避行為二", "宜避行為三"],
  "food_tip": "日常飲品或餐點",
  "mantra": "一句話心態金句"
}}"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.9,
                response_mime_type="application/json"
            )
        )
        text = response.text.strip() if getattr(response, "text", None) else ""
        if "```" in text:
            text = text.split("