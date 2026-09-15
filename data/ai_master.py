import os
import json
from google import genai
from google.genai import types

def get_ai_fortune(bazi, day_master, day_profile, distribution, useful_element, focus_topic="事業方向"):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "poem": "平心靜氣迎晨光，順應直覺最心寬。\n不急不躁走己路，好運自然到身邊。",
            "analysis": "目前處於離線模式。今天先別急著做重大決定，放慢腳步喝杯水，專注眼前手頭的事最重要。",
            "good": ["專注做完手頭最重要的一件事", "整理辦公桌或刪理手機相簿", "晚上早半小時上床休息"],
            "bad": ["衝動答應別人的臨時請求", "把時間浪費在無效爭論上", "熬夜滑手機內耗心神"],
            "food_tip": "溫熱無糖花草茶",
            "mantra": "別人的節奏是別人的，我走好自己的步調就好。"
        }

    client = genai.Client(api_key=api_key)
    dist_str = ", ".join([f"{item['name']}: {item['percent']}%" for item in distribution])

    prompt = f"""
你是一位說話親切、通俗易懂、像朋友一樣溫暖且有智慧的現代生活指引師。
請拋棄晦澀難懂的八字術語（不要直接講「土多金埋」、「日元衰旺」、「比劫」等生硬詞彙），全部轉化為現代大白話、生活化的比喻。

【用戶的排盤特質】
- 本命性格：{day_master}（{day_profile.get('nature', '')}），特質：{day_profile.get('traits', '')}
- 五行能量分佈：{dist_str}
- 偏弱、需要補充的能量：{useful_element}
- 當前最關心的重心：{focus_topic}

【請生成以下 5 項內容，語氣務必通俗、溫暖、有穿透力】：
1. poem: 一首四句短詩（不要太文言，簡單易懂、正面鼓舞）。
2. analysis: 針對「{focus_topic}」的深度解讀（120字以內）。請用白話說出他目前的狀態像什麼（例如：像一台開太多分頁而變慢的手機），並給出 1~2 個今天就能照著做的小建議。
3. good: 3 個今天最適合做的白話具體小行動（陣列格式）。
4. bad: 3 個今天最容易踩雷或內耗的行為（陣列格式）。
5. food_tip: 一款符合補充「{useful_element}」能量的日常飲料或食物（如：冰美式、豆漿、抹茶）。
6. mantra: 一句 15 字以內、能讓人瞬間放下焦慮的心態金句。

請嚴格按照以下 JSON 格式回傳，不得加入多餘文字或 markdown 區塊標記：
{{
  "poem": "四句短詩，換行用 \\n",
  "analysis": "白話易懂的分析與建議",
  "good": ["宜做事項1", "宜做事項2", "宜做事項3"],
  "bad": ["宜避事項1", "宜避事項2", "宜避事項3"],
  "food_tip": "開運飲食",
  "mantra": "防焦慮金句"
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                response_mime_type="application/json"
            )
        )
        text = response.text.strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return {
            "poem": "平心靜氣迎晨光，順應直覺最心寬。\n不急不躁走己路，好運自然到身邊。",
            "analysis": f"你天生是{day_master}特質，今天在「{focus_topic}」上容易覺得思緒有點滿。記得少看點雜七雜八的資訊，先專注在最想做的那件事就好。",
            "good": ["把代辦事項砍到只剩三件", "去戶外散步走動十分鐘", "跟能讓你笑的朋友聊兩句"],
            "bad": ["過度放大別人的無心發言", "事情還沒做就先焦慮結果", "報復性熬夜"],
            "food_tip": "一杯溫溫的蜂蜜檸檬水",
            "mantra": "先完成，再完美；慢慢來，反而更快。"
        }