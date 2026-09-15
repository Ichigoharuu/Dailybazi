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

def _extract_text_safely(response):
    """多層防禦抽取模型回傳字串，防止 NoneType 與封裝結構解析失靈"""
    if not response:
        return None

    # 1. 優先取標準 text 屬性
    try:
        if hasattr(response, "text") and response.text:
            cleaned = str(response.text).strip()
            if cleaned:
                return cleaned
    except Exception:
        pass

    # 2. 深入 candidates 結構解析
    try:
        if getattr(response, "candidates", None) and response.candidates:
            parts = response.candidates[0].content.parts
            text_parts = [getattr(p, "text", "") for p in parts if getattr(p, "text", None)]
            full_text = "".join(text_parts).strip()
            if full_text:
                return full_text
    except Exception:
        pass

    return None

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

    system_instruction = (
        "你是一位說話親切、通俗易懂、像好朋友一樣溫暖且有智慧的現代生活命理導師。"
        "嚴格禁止使用「土多金埋」、「日元旺衰」、「比劫剋財」等術語，請完全轉化為生活化大白話。"
    )

    prompt = f"""【命主排盤特質】
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

請嚴格按照以下 JSON 格式回傳：
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
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.9,
                response_mime_type="application/json"
            )
        )
        
        raw_text = _extract_text_safely(response) or ""
        fence = chr(96) * 3
        if fence in raw_text:
            raw_text = raw_text.split(fence)[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        return json.loads(raw_text.strip())
    except Exception as e:
        print(f">>> [AI Fortune Error]: {type(e).__name__} - {e}")
        return {
            "poem": f"歲月悠悠映日光，{day_master}臨風立世旁。\n莫向浮名爭短長，靜聽松風步自康。",
            "analysis": f"你的本質帶著{day_master}的堅定，面對「{focus_topic}」若感到停滯，是因為近期思緒偏滿。多調和{useful_element}的從容氣場，給自己留點留白時間。",
            "good": ["清理掉拖延已久的單項小事", "多喝溫水保持呼吸深長", "給自己安排 15 分鐘放空時間"],
            "bad": ["在疲憊時做重大承諾", "跟觀念不合的人糾結對錯", "把所有事情都攬在自己身上"],
            "food_tip": "一杯暖心黑豆水或熱美式",
            "mantra": "把心收回當下，一切自有其時。"
        }

def consult_ai_master(bazi_summary, question):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "大師目前靜思入定中，暫無法連線，請稍後再試。"

    client = genai.Client(api_key=api_key)

    clean_summary = str(bazi_summary).replace("\n", " ").strip()
    clean_question = str(question).replace("\n", " ").strip()

    system_instruction = (
        "你是一位精通子平八字與現代生活心理諮商的命理導師。"
        "回答語氣溫和、篤定、直截了當且完全通俗。"
        "嚴格禁止使用生僻術語，字數必須控制在 100 字以內，針對求問者的問題給出務實的行動策略。"
    )

    user_query = f"【命主八字背景】{clean_summary}\n【求問疑惑】{clean_question}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=300
            )
        )

        extracted = _extract_text_safely(response)
        if extracted:
            return extracted

        print(">>> [Consult Warning]: Model returned empty content.")
        return "大師推演此時氣場以守為先，眼前專注蓄力，時機成熟時自會水到渠成。"

    except Exception as e:
        print(f">>> [Consult Exception Detail]: {type(e).__name__} - {e}")
        return "大師推演此時動靜皆有機緣，把眼前的準備做好，方向自會明朗。"