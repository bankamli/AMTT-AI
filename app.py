import streamlit as st
from google import genai

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="Rollomatic AI Assistant", page_icon="🤖")
st.title("🤖 Rollomatic & VirtualGrind Pro Assistant")

# รับ API Key จากผู้ใช้งานผ่าน Sidebar
api_key = st.sidebar.text_input("กรอก Gemini API Key:", type="password")

# ปุ่มสำหรับล้างประวัติการสนทนา
if st.sidebar.button("เริ่มการสนทนาใหม่ (Clear Chat)"):
    st.session_state.messages = []
    st.rerun()

# ตัวเก็บประวัติการสนทนา
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติการสนทนาเก่า
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if api_key:
    # รับคำถามจากผู้ใช้
    if user_prompt := st.chat_input("พิมพ์คำถามเกี่ยวกับ Rollomatic หรือ VirtualGrind Pro..."):
        # แสดงข้อความผู้ใช้
        st.chat_message("user").markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        try:
            # สร้าง Client ใหม่สดๆ ทุกครั้งที่กดส่งข้อความ เพื่อป้องกัน Connection Closed
            client = genai.Client(api_key=api_key)
            
            # แปลงประวัติการสนทนาให้ตรงรูปแบบของ API
            contents = []
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })

            # เรียกใช้งาน Gemini 2.5 Flash
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents
            )

            # แสดงคำตอบจาก AI
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("👈 กรุณากรอก API Key ที่แถบด้านซ้ายก่อนเริ่มใช้งานครับ")
