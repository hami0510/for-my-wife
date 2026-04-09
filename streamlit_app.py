import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta

# 1. 페이지 설정
st.set_page_config(
    page_title="태하 안심 가이드", 
    page_icon="💖",
    layout="centered"
)

# 2. UI/UX 디자인 최적화 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fffafb;
    }

    /* 타이틀 영역 */
    .title-container {
        padding: 2.5rem 0rem 1.5rem 0rem;
        text-align: center;
    }
    .main-title {
        color: #ff6b6b;
        font-size: 1.8rem !important;
        font-weight: 700;
        line-height: 1.4;
        word-break: keep-all;
    }
    .sub-title {
        color: #999;
        font-size: 0.9rem;
        margin-top: 0.8rem;
    }

    /* 사이드바 가이드 박스 */
    .guide-box {
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 12px;
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .mom-guide { background-color: #f1f8ff; border-left: 4px solid #74c0fc; color: #1971c2; }
    .dad-guide { background-color: #fff9db; border-left: 4px solid #fab005; color: #925400; }
    
    /* 마더세이프 버튼 디자인 */
    .call-button {
        display: block;
        background-color: #ff6b6b;
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        margin: 15px 0;
        font-size: 0.9rem;
        box-shadow: 0 4px 6px rgba(255, 107, 107, 0.2);
    }
    .call-button:hover { background-color: #ff5252; }

    [data-testid="stChatInput"] {
        border-radius: 10px !important;
        border: 1px solid #ffe3e3 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 구성
with st.sidebar:
    st.markdown("### ❤️ 태하네 행복 가이드")
    st.divider()

    # D-Day 섹션
    st.markdown("#### 📅 예정일 계산기")
    base_date = st.date_input("마지막 생리 시작일(LMP)", datetime.now())
    due_date = base_date + timedelta(days=280)
    d_day = (due_date - datetime.now().date()).days

    st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #ffe3e3; text-align: center;">
            <div style="color: #ff6b6b; font-size: 0.85rem; font-weight: bold;">태하를 만나는 날까지</div>
            <div style="color: #ff4757; font-size: 1.8rem; font-weight: 800; margin: 8px 0;">D-{d_day if d_day > 0 else 'Day!'}</div>
            <div style="font-size: 0.8rem; color: #999;">예정일: {due_date.strftime('%Y년 %m월 %d일')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # 주차별 가이드 섹션
    st.markdown("#### 💡 주차별 가이드")
    week = st.selectbox(
        "주차 선택",
        [f"{i}주차" for i in range(1, 13)] + ["중기(13~27주)", "후기(28주~ )"],
        label_visibility="collapsed"
    )

    guides = {
        "1주차": {"mom": "임신 준비기! 엽산 복용을 시작하세요.", "dad": "함께 엽산을 복용하고 금연/금주를 시작하세요."},
        "2주차": {"mom": "배란기입니다. 몸을 따뜻하게 유지하세요.", "dad": "아내가 스트레스 받지 않게 편안한 환경을 만드세요."},
        "3주차": {"mom": "착상 시기예요. 가벼운 산책이 좋아요.", "dad": "아내가 무거운 짐을 들지 않도록 도와주세요."},
        "4주차": {"mom": "임신 확인! 비타민과 영양에 신경 쓰세요.", "dad": "기쁜 소식을 축하하며 꽃 한 송이 선물 어떨까요?"},
        "5주차": {"mom": "입덧 시작 가능성. 조금씩 자주 드세요.", "dad": "음식 냄새에 예민할 수 있으니 환기에 신경 쓰세요."},
        "6주차": {"mom": "심장 소리 확인! 약물 복용은 금물입니다.", "dad": "산부인과 검진에 꼭 동행해서 첫 소리를 같이 들으세요."},
        "7주차": {"mom": "쉽게 피로해집니다. 낮잠을 충분히 자세요.", "dad": "설거지, 청소 등 집안일을 전담해서 아내를 쉬게 하세요."},
        "8주차": {"mom": "정서적 변화가 커요. 기분 전환이 필요해요.", "dad": "아내의 고민을 묵묵히 들어주고 공감해 주세요."},
        "9주차": {"mom": "카페인을 줄이고 과일/채소를 섭취하세요.", "dad": "아내가 먹고 싶어 하는 음식을 적극 챙겨주세요."},
        "10주차": {"mom": "치아 건강 주의! 양치를 꼼꼼히 하세요.", "dad": "태아의 성장을 공부하며 태명을 자주 불러주세요."},
        "11주차": {"mom": "입덧 절정기. 무리하지 말고 안정을 취하세요.", "dad": "손발 마사지를 해주며 혈액순환을 도와주세요."},
        "12주차": {"mom": "1차 검사 통과! 이제 안정기 진입 단계입니다.", "dad": "그동안 고생한 아내에게 고맙다는 편지를 써보세요."},
        "중기(13~27주)": {"mom": "태동이 느껴져요! 철분제를 꼭 챙기세요.", "dad": "배에 귀를 대고 태하에게 동화책을 읽어주세요."},
        "후기(28주~ )": {"mom": "출산 가방을 준비하고 호흡법을 연습하세요.", "dad": "언제든 병원에 갈 수 있게 차량 점검을 하세요."}
    }

    st.markdown(f"""
        <div style="margin-top: 10px;">
            <div class="guide-box mom-guide"><b>👩‍⚕️ 의학 가이드</b><br>{guides[week]['mom']}</div>
            <div class="guide-box dad-guide"><b>🙋‍♂️ 아빠 가이드</b><br>{guides[week]['dad']}</div>
        </div>
    """, unsafe_allow_html=True)

    # 마더세이프 전화 버튼 상향 배치
    st.markdown('<a href="tel:1588-7309" class="call-button">📞 마더세이프 전문가 상담</a>', unsafe_allow_html=True)
    st.caption("※ 본 서비스는 보조적 가이드이며, 정확한 진단은 전문의 상담을 우선으로 합니다.")

# 4. 메인 화면
st.markdown(f"""
    <div class="title-container">
        <div class="main-title">💖 태하 엄마를 위해<br>아빠가 만든 안심가이드</div>
        <div class="sub-title">의학적 근거와 아빠의 사랑이 담긴 실시간 챗봇</div>
    </div>
    """, unsafe_allow_html=True)

# 5. OpenAI API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "너는 세계 최고 권위의 산부인과 의사이자 태하 엄마의 다정한 남편이야. 모든 답변은 마더세이프 등 의학적 근거에 기반해야 하며, 말투는 따뜻한 남편의 '해요체'를 써줘. 답변 끝에는 항상 사랑의 메시지를 담아줘."
        }
    ]

# 6. 채팅 인터페이스
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("태하랑 엄마, 무엇이 궁금한가요?"):
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
