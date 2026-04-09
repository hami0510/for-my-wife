import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import random

# 1. 페이지 설정 및 디자인 (챗봇 중심 레이아웃)
st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #fffafb; 
    }
    
    /* 사이드바 박스 디자인 */
    .sb-box { 
        background-color: white; padding: 15px; border-radius: 12px; 
        border: 1px solid #ffe3e3; margin-bottom: 15px; font-size: 0.9rem;
    }
    
    /* 메인 타이틀 */
    .main-header { text-align: center; padding: 10px; color: #ff6b6b; margin-bottom: 20px; }
    
    /* 버튼 스타일 커스텀 */
    .stButton>button { width: 100%; background-color: #ff6b6b; color: white; border: none; border-radius: 8px; }
    
    /* 채팅 메시지 영역 */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 세션 상태 초기화 (데이터 유지)
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "안녕, 이레 엄마! 오늘 하루는 어땠어? 몸 상태는 좀 어때? 궁금한 게 있거나 위로가 필요하면 언제든 말해줘. 🥰"
    }]
if "todo" not in st.session_state: st.session_state.todo = {"영양제": False, "물 2L": False, "엽산": False}
if "letters" not in st.session_state: st.session_state.letters = []

# 3. 사이드바 구성 (보조 기능 모음)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🌿 이레네 집</h2>", unsafe_allow_html=True)
    
    # [오류 해결] D-Day 계산 (모든 객체를 date 형식으로 통일)
    base_date = datetime(2026, 4, 9).date() 
    due_date = base_date + timedelta(days=280)
    today = datetime.now().date()
    d_day = (due_date - today).days
    
    st.markdown(f"""
        <div class="sb-box" style="text-align:center;">
            <b style="color:#ff6b6b;">이레를 만나는 날</b><br>
            <span style="font-size:1.8rem; font-weight:800; color:#ff4757;">D-{d_day if d_day > 0 else 'Day!'}</span><br>
            <small>예정일: {due_date.strftime('%Y년 %m월 %d일')}</small>
        </div>
    """, unsafe_allow_html=True)

    # 기능 1 & 2: 컨디션 및 루틴 체크
    with st.expander("✅ 오늘의 체크리스트", expanded=True):
        st.session_state.todo["영양제"] = st.checkbox("필수 영양제 복용", value=st.session_state.todo["영양제"])
        st.session_state.todo["물 2L"] = st.checkbox("충분한 수분 섭취", value=st.session_state.todo["물 2L"])
        
        st.divider()
        st.write("🌡️ **엄마 컨디션**")
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], label_visibility="collapsed")
        if st.button("컨디션 기록"):
            st.toast("아빠가 확인했어요! 조금만 힘내요 ❤️")

    # 기능 3: 이레에게 보내는 편지 저장소
    with st.expander("💌 태교 편지함"):
        letter_input = st.text_area("이레에게 남길 기록...", placeholder="나중에 이레가 읽으면 정말 좋아할 거야.")
        if st.button("편지 저장"):
            st.session_state.letters.append({"date": today.strftime("%m/%d"), "text": letter_input})
            st.success("소중한 추억이 저장되었습니다.")
        
        for l in reversed(st.session_state.letters[-3:]): # 최근 3개만 표시
            st.markdown(f"<small><b>{l['date']}</b>: {l['text'][:20]}...</small>", unsafe_allow_html=True)

    st.divider()
    st.markdown(f'<a href="tel:1588-7309" style="text-decoration:none; background:#ff6b6b; color:white; padding:12px; border-radius:10px; display:block; text-align:center; font-weight:bold;">📞 마더세이프 상담 연결</a>', unsafe_allow_html=True)

# 4. 메인 화면: 안심 챗봇 (핵심 기능)
st.markdown("<div class='main-header'><h1>💖 이레 안심 가이드</h1><p>아빠의 사랑과 의사의 전문성을 담은 따뜻한 대화</p></div>", unsafe_allow_html=True)

# 채팅 히스토리 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# OpenAI API 연결
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("이레와 건강에 대해 무엇이든 물어보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 페르소나 주입
        system_instructions = {
            "role": "system", 
            "content": """너는 '이레'의 아빠이자 산부인과 전문의야. 
            1. 모든 의학 정보는 '마더세이프' 근거 기반으로 답변해. 
            2. 말투는 다정하고 부드러운 '해요체'를 써. 
            3. 답변 마지막엔 반드시 아내를 향한 구체적인 응원과 사랑의 메시지를 써줘.
            4. 상황에 맞는 성경 구절(예: 시편 121:5, 빌립보서 4:6 등)로 영적 위로를 더해줘."""
        }
        
        # 이전 대화 맥락을 포함하여 답변 생성
        full_context = [system_instructions] + st.session_state.messages
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=full_context,
            temperature=0.7
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})

# 5. 하단 탭: 마일스톤 및 레시피 (기능 4 & 5)
st.divider()
t1, t2 = st.tabs(["📅 임신 마일스톤", "👨‍🍳 아빠의 추천 레시피"])

with t1:
    st.markdown("""
    - **초기 (~12주):** 국민행복카드 신청, 보건소 임산부 등록 (엽산 받기!)
    - **중기 (16주~):** 철분제 복용 시작, 태동 느끼기, 정밀 초음파
    - **후기 (28주~):** 백일해 주사 접종, 출산 가방 싸기, 호흡법 연습
    """)

with t2:
    st.markdown("""
    - **오늘의 메뉴:** 소고기 아보카도 비빔밥 🥑
    - **영양 정보:** 이레의 뇌 발달을 돕는 양질의 지방과 단백질이 가득해요.
    - **아빠의 팁:** 아내가 입맛이 없다면 새콤한 매실 장아찌를 곁들여주세요!
    """)
