import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta

# 1. 페이지 설정
st.set_page_config(
    page_title="태하 안심 가이드", 
    page_icon="💖",
    layout="centered"
)

# 2. 레이아웃 및 디자인 최적화 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fffafb;
    }

    .title-container {
        padding: 1.5rem 0rem 1rem 0rem;
        text-align: center;
    }
    .main-title {
        color: #ff6b6b;
        font-size: 1.8rem !important;
        font-weight: 700;
        line-height: 1.3;
        word-break: keep-all;
    }
    .sub-title {
        color: #888;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* 사이드바 D-Day 카드 디자인 */
    .dday-card {
        background-color: #fff0f3;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #ffccd5;
        margin-bottom: 10px;
    }
    .dday-title { color: #ff6b6b; font-size: 0.8rem; font-weight: bold; }
    .dday-value { color: #ff4757; font-size: 1.5rem; font-weight: 800; }

    .stChatMessage { border-radius: 15px; max-width: 90%; }
    .stChatInputContainer { padding-bottom: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 구성 (기능 추가)
with st.sidebar:
    st.markdown("### ❤️ 태하네 행복 가이드")
    st.divider()

    # --- 분만예정일 계산 섹션 ---
    st.markdown("#### 📅 예정일 계산기")
    # 기준일 입력 (마지막 생리 시작일 또는 확인일 기준)
    base_date = st.date_input("마지막 생리 시작일(LMP)을 입력하세요", datetime.now())
    
    # 분만예정일 계산 (280일 기준)
    due_date = base_date + timedelta(days=280)
    # 디데이 계산
    today = datetime.now().date()
    d_day = (due_date - today).days

    # D-Day 표시 레이아웃
    st.markdown(f"""
        <div class="dday-card">
            <div class="dday-title">태하를 만나는 날까지</div>
            <div class="dday-value">D-{d_day if d_day > 0 else 'Day!'}</div>
            <div style="font-size: 0.8rem; color: #555; margin-top:5px;">
                예정일: {due_date.strftime('%Y년 %m월 %d일')}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # --- 주차별 정보 섹션 ---
    st.markdown("#### 💡 주차별 의학 가이드")
    week = st.selectbox(
        "주차를 선택하세요",
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
    st.success(week_info[week])
    
    st.divider()
    st.write("📞 마더세이프: 1588-7309")

# 4. 메인 화면 타이틀
st.markdown(f"""
    <div class="title-container">
        <div class="main-title">💖 태하 엄마를 위해<br>아빠가 만든 안심가이드</div>
        <div class="sub-title">전 세계 최고 권위 의사의 지식과 아빠의 사랑을 담았습니다.</div>
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

# 6. 채팅 인터페이스
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
