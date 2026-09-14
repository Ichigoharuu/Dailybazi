import os
import json
from google import genai

def get_ai_fortune(bazi, day_master, day_profile, distribution, useful_element):
    """
    呼叫 Gemini API，根據命盤結構生成專屬命理大師解讀。
    若無 API Key 或連線失敗，自動啟用優雅的備援離線解盤。
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "poem": "天道自然有定數，順應本心自得安。",
            "analysis": "目前處於離線靜思模式。調和內在氣息，專注於當下即是最好的開運之道。"
        }

    client = genai.Client(api_key=api_key)

    dist_str = ", ".join([f"{item['name']}: {item['percent']}%" for item in distribution])
    
    prompt = f"""
你是一位深諳子平八字與東方生命哲學的當代玄學導師，語氣深邃、沉穩、優雅且富有同理心，拒絕恐嚇與陳腐迷信，擅長以心理學和能量流動的角度啟發問命者。

【命主排盤參數】
- 四柱八字：年柱[{bazi['year']}]、月柱[{bazi['month']}]、日柱[{bazi['day']}]、時柱[{bazi['hour']}]
- 日主本命：{day_master}（{day_profile.get('nature', '')}）
- 原型特質：{day_profile.get('traits', '')}
- 五行氣場分佈：{dist_str}
- 偏弱需調和元素（喜用方向）：{useful_element}

請為命主提供以下兩項專屬解讀：
1. 【命理大師·今日籤詩】：以典雅的四句七言詩作結，點出命主當前的修行重心與氣場流轉。
2. 【能量破局·深度解盤】：以 120 字以內的精煉文字，解析其日主與五行能量的平衡之道，並給予一條極具啟發性的心態調適指引。

請嚴格按照以下 JSON 格式回傳，不要加入額外 markdown 標記：
{{
  "poem": "七言詩四句（以逗號或換行分隔）",
  "analysis": "120字以內的深度解盤與開運指南"
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text.strip())
        return data
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return {
            "poem": "天地玄黃存定數，順時而動自安然。",
            "analysis": f"命主日元為{day_master}，當前氣場以調和{useful_element}為要。靜心守正，自有貴人相助。"
        }