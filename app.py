import streamlit as st
from google import genai
from google.genai.errors import APIError

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="Rollomatic AI Assistant", page_icon="🤖")
st.title("🤖 Rollomatic & VirtualGrind Pro Assistant")

# รับ API Key จากผู้ใช้งานผ่าน Sidebar
api_key = st.sidebar.text_input("กรอก Gemini API Key:", type="password")

# ปุ่มสำหรับเริ่มบทสนทนาใหม่
if st.sidebar.button("เริ่มการสนทนาใหม่ (Clear Chat)"):
    st.session_state.pop("chat_session", None)
    st.session_state.pop("messages", None)
    st.rerun()

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # สร้าง Chat Session หากยังไม่มี
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = client.chats.create(model="gemini-3.6-flash")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # แสดงประวัติการสนทนา
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # รับคำถามและส่งหา AI
        if user_prompt := st.chat_input("พิมพ์คำถามเกี่ยวกับ Rollomatic หรือ VirtualGrind Pro..."):
            st.chat_message("user").markdown(user_prompt)
            st.session_state.messages.append({"role": "user", "content": user_prompt})

            try:
                response = st.session_state.chat_session.send_message(user_prompt)
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการส่งข้อความ: {e}")
                st.info("💡 หากเพิ่งเปลี่ยน API Key ใหม่ กรุณากดปุ่ม 'เริ่มการสนทนาใหม่' ที่แถบด้านซ้ายมือครับ")

    except Exception as e:
        st.error(f"การเชื่อมต่อ API ล้มเหลว: {e}")
else:
    st.info("👈 กรุณากรอก API Key ที่สร้างใหม่จาก Google AI Studio ที่แถบด้านซ้ายก่อนเริ่มใช้งานครับ")
