import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(page_title="태하 엄마를 위한 안심 가이드", page_icon="💖")

# 2. 디자인 테마 (핑크색 포인트)
st.markdown("""
    <style>
    .stApp { background-color: #fffafb; }
    h1 { color: #ff6b6b; font-family: 'Nanum Gothic', sans-serif; }
    .stChatMessage { border-radius: 15px; }
    .sidebar-text { font-size: 14px; color: #555; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 구성 (주차별 정보 섹션)
with st.sidebar:
    st.header("❤️ 태하네 행복 가이드")
    st.write("태하 엄마를 위해 아빠가 만든 안심가이드")
    st.divider()

    # 주차별 정보 섹션
    st.subheader("📅 주차별 안심 정보")
    week = st.selectbox(
        "현재 임신 주차를 선택하세요",
        [f"{i}주차" for i in range(1, 13)] + ["중기(13~27주)", "후기(28주~ )"]
    )

    # 주차별 팁 데이터
    week_info = {
        "1주차": "임신 준비기입니다. 엽산을 꼭 챙겨 드세요!",
        "2주차": "배란기예요. 편안한 마음가짐이 가장 중요합니다.",
        "3주차": "수정란이 자리를 잡는 시기예요. 무리한 운동은 피해주세요.",
        "4주차": "테스트기로 확인 가능한 시기! 아기집을 기다려봐요.",
        "5주차": "심장 소리를 들을 수 있어요. 입덧이 시작될 수 있으니 조금씩 자주 드세요.",
        "6주차": "아기의 뇌와 중추신경이 발달해요. 약물 복용에 특히 주의하세요.",
        "7주차": "손발이 형성되는 시기예요. 충분한 휴식이 필요합니다.",
        "8주차": "태아의 움직임이 시작돼요. 아빠의 다정한 목소리를 들려주세요.",
        "9주차": "얼굴 윤곽이 잡혀요. 변비가 생길 수 있으니 수분을 충분히 섭취하세요.",
        "10주차": "기관 형성이 거의 완료돼요. 스트레스는 금물!",
        "11주차": "입덧이 절정일 수 있어요. 먹을 수 있는 음식을 찾아 조금씩 드세요.",
        "12주차": "1차 기형아 검사 시기예요. 이제 안정기에 접어들고 있어요!",
        "중기(13~27주)": "입덧이 가라앉고 배가 나오기 시작해요. 철분제를 꼭 챙겨 드세요.",
        "후기(28주~ )": "숨이 차고 몸이 무거워져요. 출산 준비물을 체크해 볼까요?"
    }
    
    st.info(week_info[week])
    
    st.divider()
    st.subheader("📌 꼭 기억하세요")
    st.write("📞 마더세이프: 1588-7309")
    st.caption("이 앱은 남편이 아내를 위해 만든 보조 가이드입니다. 정확한 의학적 판단은 주치의와 상의하세요.")

# 4. 메인 화면 타이틀
st.title("💖 태하 엄마를 위해 아빠가 만든 안심가이드")
st.write("궁금한 음식이나 약물, 증상을 물어보세요. 마더세이프 정보를 기반으로 답해드려요.")

# 5. OpenAI API 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "너는 '마더세이프' 가이드를 숙지한 임신 전문 상담사야. 사용자는 너의 아내 '태하 엄마'야. 너는 태하 아빠처럼 아주 다정하고 따뜻하게 말해야 해. 말투는 '해요체'를 쓰고, 음식/약물 질문에는 마더세이프 기준을 엄격히 따르되 답변 끝에는 항상 태하 엄마를 향한 사랑의 메시지나 응원을 덧붙여줘."
        }
    ]

# 6. 채팅 로직
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("오늘 태하랑 엄마 컨디션은 어때요?"):
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
