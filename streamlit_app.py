import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="햇살이 엄마를 위한 안심 가이드", page_icon="💖")

# 디자인 테마
st.markdown("""
    <style>
    .stApp { background-color: #fffafb; }
    h1 { color: #ff6b6b; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💖 아내를 위한 안심 가이드")
st.write("마더세이프 정보를 기반으로 다정하게 답해드려요.")

# 사이드바 설정
with st.sidebar:
    st.header("📌 꼭 기억하세요")
    st.write("📞 마더세이프: 1588-7309")
    st.divider()
    st.info("이 서비스는 남편이 아내를 위해 만든 개인용 가이드입니다. 정확한 의학적 판단은 반드시 주치의와 상의하세요.")

# API 키 설정 (Streamlit Secrets에서 불러옴)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "너는 임산부 약물 상담 전문기관 '마더세이프'의 정보를 숙지한 다정한 상담사야. 사용자는 너의 소중한 아내야. 말투는 항상 남편처럼 따뜻하고 부드럽게 '해요체'를 써줘. 음식, 약물 질문에 대해 마더세이프 기준을 충실히 답해주고, 끝에는 항상 '사랑해' 혹은 '우리 아기랑 같이 힘내자' 같은 응원을 잊지 마."}
    ]

# 채팅 인터페이스
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("오늘 궁금한 게 있나요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
