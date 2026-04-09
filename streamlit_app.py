import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import random

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #fffafb; 
    }
    .main-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stButton>button { background-color: #ff6b6b; color: white; border: none; border-radius: 8px; }
    .stCheckbox { color: #ff6b6b; }
    h1, h2, h3 { color: #ff6b6b; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 세션 상태 초기화 (기록용)
if "condition_log" not in st.session_state: st.session_state.condition_log = []
if "letters" not in st.session_state: st.session_state.letters = []
if "todo" not in st.session_state: st.session_state.todo = {"영양제": False, "물 2L": False, "엽산": False}

# 3. 사이드바 구성 (예정일 및 마더세이프)
with st.sidebar:
    st.title("💖 이레네 집")
    # [기존 로직: D-Day 계산기]
    base_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9))
    due_date = base_date + timedelta(days=280)
    d_day = (due_date - datetime.now().date()).days
    st.metric(label="이레 만나는 날", value=f"D-{d_day}")
    st.write(f"예정일: {due_date.strftime('%Y-%m-%d')}")
    
    st.divider()
    st.markdown(f'<a href="tel:1588-7309" style="text-decoration:none; background:#ff6b6b; color:white; padding:10px; border-radius:10px; display:block; text-align:center;">📞 마더세이프 연결</a>', unsafe_allow_html=True)

# 4. 메인 화면 레이아웃 (2개 컬럼)
col1, col2 = st.columns([1, 1])

with col1:
    # 기능 1: 컨디션 기록 (Daily Log)
    st.subheader("🌡️ 오늘 엄마 컨디션")
    with st.container():
        cond = st.select_slider("오늘 컨디션은 어때요?", options=["매우 힘듦", "조금 지침", "보통", "좋음", "최상!"])
        note = st.text_input("아빠에게 한마디 (예: 입덧이 심해..)")
        if st.button("컨디션 기록하기"):
            st.session_state.condition_log.append({"date": datetime.now(), "cond": cond, "note": note})
            st.toast("아빠에게 컨디션이 전달되었어요! ❤️")

    # 기능 2: 영양제/수분 체크 (To-Do)
    st.subheader("✅ 꼭 챙겨야 할 루틴")
    st.session_state.todo["영양제"] = st.checkbox("오늘의 필수 영양제 복용", value=st.session_state.todo["영양제"])
    st.session_state.todo["물 2L"] = st.checkbox("이레를 위한 충분한 수분 섭취", value=st.session_state.todo["물 2L"])
    st.session_state.todo["엽산"] = st.checkbox("엽산 챙겨 먹기", value=st.session_state.todo["엽산"])

with col2:
    # 기능 3: 이레에게 보내는 편지 (Moment Archive)
    st.subheader("💌 이레에게 쓰는 편지")
    with st.expander("오늘의 기록 남기기"):
        letter_content = st.text_area("이레에게 하고 싶은 말...")
        if st.button("저장하기"):
            st.session_state.letters.append({"date": datetime.now().strftime("%y.%m.%d"), "content": letter_content})
    
    if st.session_state.letters:
        last_letter = st.session_state.letters[-1]
        st.info(f"📅 {last_letter['date']}: {last_letter['content']}")

# 5. 하단 섹션 (마일스톤 & 레시피)
st.divider()
tab1, tab2, tab3 = st.tabs(["📅 임신 마일스톤", "👨‍🍳 아빠의 추천 레시피", "🤖 안심 챗봇"])

with tab1:
    # 기능 4: 시기별 체크리스트
    st.markdown("""
    ### 🚩 시기별 꼭 해야 할 일
    * **~12주:** 보건소 임산부 등록 (선물 챙기기!), 국민행복카드 신청
    * **16주~20주:** 철분제 복용 시작, 2차 기형아 검사
    * **24주~28주:** 입체 초음파, 임신성 당뇨 검사
    """)

with tab2:
    # 기능 5: 아빠의 태담 요리 레시피
    st.markdown("""
    ### 🥩 이레 엄마를 위한 영양 레시피
    **[오늘의 추천: 소고기 아보카도 덮밥]**
    * **이유:** 아기의 뇌 발달에 좋은 엽산과 단백질이 풍부해요!
    * **준비물:** 소고기 우둔살, 잘 익은 아보카도, 계란 노른자
    * **아빠의 팁:** 아보카도를 으깨서 부드럽게 만들어주면 아내가 먹기 편해요.
    """)

with tab3:
    # 기존 기능: 안심 챗봇
    st.write("의학적인 궁금증이나 위로가 필요할 때 언제든 물어보세요.")
    # (챗봇 코드 생략 - 이전 버전과 동일하게 배치 가능)
    st.text_input("질문을 입력하세요...", key="chat_input")

# 마지막 사랑의 메시지
st.markdown(f"---")
st.markdown(f"<h3 style='text-align: center;'>이레 엄마, 오늘도 이레를 품어줘서 고마워요. 사랑해! ❤️</h3>", unsafe_allow_html=True)
