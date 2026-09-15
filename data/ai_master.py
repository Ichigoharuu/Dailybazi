import os
import json
import random
import sys
import re
from google import genai
from google.genai import types

RANDOM_PERSPECTIVES = [
    "微風拂面、枝芽初綻之生機",
    "烈火淬金、淬鍊鋒芒之篤定",
    "厚土負載、沉穩蓄力之踏實",
    "秋水長天、沉靜收斂之清朗",
    "清泉繞石、隨順變通之智慧"
]

def _extract_text(response):
    """防禦性安全抽取文字"""
    if not response:
        return None
    try:
        if getattr(response, "text", None):
            cleaned = str(response.text).strip()
            if cleaned:
                return cleaned
    except Exception:
        pass

    try:
        if getattr(response, "candidates", None) and response.candidates:
            cand = response.candidates[0]
            if cand.content and cand.content.parts:
                texts = [str(p.text) for p in cand.content.parts if getattr(p, "text", None)]
                combined = "".join(texts).strip()
                if combined:
                    return combined
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
        "你是一位說話親切、通俗易懂的現代生活命理導師。"
        "嚴禁出現生硬術語（如「土多金埋」、「日元旺衰」等），完全轉化為生活化大白話。"
    )

    prompt = f"""【命主排盤特質】
- 四柱八字：[{bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}]
- 本命性格：{day_master}（{day_profile.get('nature', '')}），特質：{day_profile.get('traits', '')}
- 先天五行氣場分佈：{dist_str}
- 偏弱需調和元素：{useful_element}
- 當前問命重心：{focus_topic}
- 本次意象引導：{perspective}

請生成以下 6 項內容（JSON 格式）：
1. poem: 一首四句短詩（每句字數相仿，白話鼓舞）。
2. analysis: 針對「{focus_topic}」的白話解盤（120字以內）。
3. good: 3 個今天最適合做的白話具體小行動（字串陣列）。
4. bad: 3 個今天最容易踩雷的行為（字串陣列）。
5. food_tip: 一款補「{useful_element}」能量的日常飲品或餐點。
6. mantra: 一句 15 字以內安撫焦慮的金句。

回傳 JSON 格式如下：
{{
  "poem": "四句詩",
  "analysis": "白話分析",
  "good": ["宜1", "宜2", "宜3"],
  "bad": ["忌1", "忌2", "忌3"],
  "food_tip": "飲食推薦",
  "mantra": "金句"
}}"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.9,
                response_mime_type="application/json"
            )
        )
        raw_text = _extract_text(response) or ""
        fence = chr(96) * 3
        if fence in raw_text:
            raw_text = raw_text.split(fence)[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        return json.loads(raw_text.strip())
    except Exception as e:
        print(f">>> [AI Fortune Error]: {e}", file=sys.stderr, flush=True)
        return {
            "poem": f"歲月悠悠映日光，{day_master}臨風立世旁。\n莫向浮名爭短長，靜聽松風步自康。",
            "analysis": f"你的本質帶著{day_master}的堅定，多調和{useful_element}的從容氣場，把節奏放慢下來。",
            "good": ["清理掉拖延已久的小事", "多喝溫水保持深呼吸", "給自己安排放空時間"],
            "bad": ["在疲憊時做承諾", "跟人糾結對錯", "把所有事情攬在身上"],
            "food_tip": "一杯溫熱無糖茶飲",
            "mantra": "把心收回當下，一切自有其時。"
        }

def consult_ai_master(bazi_summary, question):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "大師目前靜思入定中，暫無法連線，請稍後再試。"

    client = genai.Client(api_key=api_key)

    clean_summary = re.sub(r'[\r\n\t\'"]+', ' ', str(bazi_summary)).strip()
    clean_question = re.sub(r'[\r\n\t\'"]+', ' ', str(question)).strip()

    engineered_prompt = (
        "【系統角色】你是一位通曉傳統八字哲學、擅長心理陪伴的現代生活導師。\n"
        "【情境說明】問命者在進行日常哲理探討與心態梳理，請從性格優勢、時機心態與行動策略給予溫暖指引，絕非迷信斷言。\n"
        f"【問命者特質】{clean_summary}\n"
        f"【問命者困惑】「{clean_question}」\n\n"
        "【回答規範】\n"
        "1. 必須在 90 字以內，直截了當給出務實、鼓舞人心的行動心態建議。\n"
        "2. 嚴格禁止使用任何生僻術語（如正財、偏官、合化等），全程使用生活大白話。\n"
        "3. 語氣溫暖篤定，像一位洞察世事的朋友在給予方向。"
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=engineered_prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                max_output_tokens=250
            )
        )

        reply = _extract_text(response)
        if reply:
            return reply

        if getattr(response, "candidates", None) and response.candidates:
            reason = getattr(response.candidates[0], "finish_reason", "UNKNOWN")
            print(f">>> [Model Finish Reason]: {reason}", file=sys.stderr, flush=True)

        return "以你命盤的韌性而言，此事動靜皆在人為。先將手頭積累做足，順勢而為自會明朗。"

    except Exception as e:
        error_type = type(e).__name__
        error_detail = str(e)
        print(f">>> [DEBUG-EXCEPTION]: {error_type} -> {error_detail}", file=sys.stderr, flush=True)
        return f"【連線異常 {error_type}】：{error_detail[:120]}"