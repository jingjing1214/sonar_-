import streamlit as st
import json
import os
from chatbot import ask_perplexity

st.set_page_config(page_title="冰箱食材推薦系統", layout="wide")
st.title("🥬 冰箱食材 X 食譜推薦")

selected_user = st.sidebar.selectbox("👤 選擇使用者", ["Charlotte", "Nono"])
username = selected_user.lower()
user_data_file = f"user_data/{username}_fridge.json"

def load_user_fridge():
    try:
        with open(user_data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return "雞肉, 馬鈴薯"

def save_user_fridge(content):
    os.makedirs("user_data", exist_ok=True)
    with open(user_data_file, "w", encoding="utf-8") as f:
        json.dump(content, f)

st.sidebar.markdown(f"目前使用者：**{selected_user}**")
ingredients = st.text_input("🧊 我的冰箱食材（用逗號分隔）", load_user_fridge())
if st.button("💾 儲存食材清單"):
    save_user_fridge(ingredients)
    st.success("✅ 已儲存你的食材清單！")

api_key = st.text_input("🔑 請輸入 Perplexity API Key", type="password")

if api_key:
    st.subheader("🍽️ AI 食譜推薦（5 道創意命名料理）")
    if st.button("推薦食譜"):
        prompt = f"""我冰箱裡有：{ingredients}。
請推薦我 5 道可以做的家常料理。每道料理請賦予有創意、有畫面感、有特色的名字（可加入形容詞、氣氛、料理方式）。請依下列格式清楚分段回覆：

🥘 食譜編號：
🍽️ 料理名稱：
🧂 所需食材：
🧑‍🍳 烹調流程：（請用 3~5 步驟分段說明）"""
        with st.spinner("AI 正在構思創意料理中..."):
            recipes = ask_perplexity(api_key, prompt)
            st.session_state["last_recipes"] = recipes

    if "last_recipes" in st.session_state:
        st.markdown(st.session_state["last_recipes"])

    st.subheader("🧠 與料理助理聊聊")
    question = st.text_input("你對上面的創意食譜有什麼問題？")
    if question:
        combined_prompt = (
            f"以下是我剛剛獲得的食譜建議：\n{st.session_state['last_recipes']}\n\n現在我有個問題：{question}"
        )
        with st.spinner("AI 助理回覆中..."):
            reply = ask_perplexity(api_key, combined_prompt)
            st.markdown(reply)
else:
    st.info("請輸入 API Key 以使用 AI 推薦功能")
