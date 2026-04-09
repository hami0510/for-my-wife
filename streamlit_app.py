import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(
    page_title="태하 안심 가이드", 
    page_icon="💖",
    layout="centered"
)

# 2. 레이아웃 및 줄맞춤 최적화 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fffafb;
    }

    /* 타이틀 중앙 정렬 및 여백 최적화 */
    .title-container {
        padding: 2rem 0rem 1.5rem 0rem;
        text-align: center;
    }
    .main-title {
        color: #ff6b6b;
        font-size: 2rem !important;
        font-weight: 700;
        line-height: 1.3;
        word-break: keep-all;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* 채팅 메시지 줄맞춤 및 디자인 */
    .stChatMessage {
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        max-width: 90%;
    }
    
    /* 사이드바 디자인 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }

    /* 입력창 하단 고정 및 중앙 정렬 최적화 */
    .stChatInputContainer {
        padding-bottom: 30px !important;
    }
    
    /* 이미지/컴포넌트 간격 조절 */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 구성
with st.sidebar:
    st.markdown("### ❤️ 태하네 행복 가이드")
    st.caption("태하 엄마를 위해 아빠가 만든 전문가급 가이드")
    st.divider()

    st.markdown("#### 📅 주차별 의학 정보")
    week = st.selectbox(
        "현재 주차를 선택하세요",
        [f"{i}주차" for i in range(1, 13)] + ["중기(13~27주)", "후기(28주~ )"],
        label_visibility="collapsed"
    )

    week_info = {
        "1주차": "마지막 생리 시작일입니다. 임신 준비를 위해 엽산 400~800mcg 복용을 시작하세요.",
        "2주차": "배란기입니다. 기초체온 변화에 유의하며 규칙적인 생활을 유지하세요.",
        "3주차": "수정 및 착상 시기입니다. 고열이나 무리한 약물 복용은 피해야 합니다.",
        "4주차": "임신 확인 가능기. 태아의 신경관이 형성되기 시작하므로 금연, 금주는 필수입니다.",
        "5주차": "아기집과 난황 확인 시기. 입덧(오심)이 시작될 수 있으며 수분 섭취가 중요합니다.",
        "6주차": "심장박동 확인 가능. 태아의 주요 장기가 형성되는 시기이므로 약물 사용 전 상담하세요.",
        "7주차": "손발 싹이 발달합니다. 충분한 수면과 균형 잡힌 영양소 섭취가 필요합니다.",
        "8주차": "태아기 진입. 태아의 움직임이 시작됩니다. 아빠와의 교감이 중요합니다.",
        "9주차": "안면 구조 형성기. 카페인 섭취를 하루 200mg 이하로 제한하세요.",
        "10주차": "태아 장기 형성 완료 단계. 스트레스 관리와 편안한 휴식이 우선입니다.",
        "11주차": "입덧 절정기. 소량씩 자주 먹는 식이요법이 권장됩니다.",
        "12주차": "1차 정밀 초음파 시기입니다. 유산 위험이 낮아지는 안정기 진입 단계입니다.",
        "중기(13~27주)": "철분제 복용을 시작하고 임신성 당뇨 검사를 준비하세요.",
        "후기(28주~ )": "백일해 접종을 고려하세요. 분만 징후를 미리 숙지해야 합니다."
    }
    
    st.success(f"**[{week} 가이드]**\n\n{week_info[week]}")
    
    st.divider()
    st.markdown("#### 📌 전문 상담 기관")
    st.write("📞 마더세이프: 1588-7309")
    st.caption("※ 본 정보는 보조적 수단이며, 실제 진단은 전문의의 진료를 우선합니다.")

# 4. 메인 화면 타이틀 (중앙 정렬 레이아웃)
st.markdown(f"""
    <div class="title-container">
        <div class="main-title">💖 태하 엄마를 위해<br>아빠가 만든 안심가이드</div>
        <div class="sub-title">추측이 아닌 의학적 근거로 태하와 엄마를 지킵니다.</div>
    </div>
    """, unsafe_allow_html=True)

# 5. OpenAI API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "너는 세계 최고 권위의 산부인과 의사이자 태하 엄마의 다정한 남편이야. 모든 답변은 마더세이프 등 의학적 근거에 기반해야 하며, 말투는 세상에서 가장 따뜻한 남편의 '해요체'를 써줘. 답변 끝에는 항상 아내를 향한 사랑의 메시지를 담아줘."
        }
    ]

# 6. 채팅 출력 (중앙 정렬 유지)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. 채팅 입력
if prompt := st.chat_input("태하랑 엄마, 궁금한 게 있나요?"):
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
