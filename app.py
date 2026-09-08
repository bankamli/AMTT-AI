import streamlit as st
from google import genai

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="Rollomatic AI Assistant", page_icon="🤖")
st.title("🤖 Rollomatic & VirtualGrind Pro Assistant")

# รับ API Key จากผู้ใช้งานผ่าน Sidebar
api_key = st.sidebar.text_input("กรอก Gemini API Key:", type="password")

# ปุ่มสำหรับล้างประวัติการสนทนา
if st.sidebar.button("เริ่มการสนทนาใหม่ (Clear Chat)"):
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

# ตัวเก็บประวัติการสนทนา
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติการสนทนาเก่า
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if api_key:
    # สร้าง Client และเตรียม Chat Session
    if "chat" not in st.session_state:
        try:
            client = genai.Client(api_key=api_key)
            st.session_state.chat = client.chats.create(model="gemini-2.5-flash")
        except Exception as e:
            st.error(f"สร้างการเชื่อมต่อไม่สำเร็จ: {e}")

    # รับคำถามจากผู้ใช้
    if user_prompt := st.chat_input("พิมพ์คำถามเกี่ยวกับ Rollomatic หรือ VirtualGrind Pro..."):
        # แสดงข้อความผู้ใช้
        st.chat_message("user").markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        try:
            # ส่งข้อความผ่าน Chat Session
            response = st.session_state.chat.send_message(user_prompt)

            # แสดงคำตอบจาก AI
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
            st.info("💡 หากเพิ่งเปลี่ยน Key ให้กดปุ่ม 'เริ่มการสนทนาใหม่ (Clear Chat)' ด้านซ้ายมือครับ")
else:
    st.info("👈 กรุณากรอก API Key ที่แถบด้านซ้ายก่อนเริ่มใช้งานครับ")
