import streamlit as st
from google import genai

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="Rollomatic AI Assistant", page_icon="🤖")
st.title("🤖 Rollomatic & VirtualGrind Pro Assistant")

# 1. รับ API Key จากผู้ใช้งาน
api_key = st.sidebar.text_input("กรอก Gemini API Key:", type="password")

if api_key:
    # สร้าง Client และเตรียม Chat Session
    client = genai.Client(api_key=api_key)
    
    # ตัวเก็บประวัติการสนทนาในความจำของ Streamlit
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = client.chats.create(model="gemini-3.6-flash")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # แสดงประวัติข้อความเก่าในหน้าแชท
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ช่องพิมพ์ข้อความคุยกับ AI (Chat Input)
    if user_prompt := st.chat_input("พิมพ์คำถามเกี่ยวกับ Rollomatic หรือ VirtualGrind Pro..."):
        # แสดงข้อความของฝั่งผู้ใช้
        st.chat_message("user").markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        # ส่งข้อความไปหา Gemini API และรอคำตอบ
        response = st.session_state.chat_session.send_message(user_prompt)

        # แสดงคำตอบจาก AI
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("....")
