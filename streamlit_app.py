import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import random

# 1. 페이지 설정 및 디자인 (챗봇 최적화 레이아웃)
st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #fffafb; 
    }
    
    /* 챗봇 메시지 스타일링 */
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    
    /* 메인 타이틀 디자인 */
    .main-header { text-align: center; padding: 20px; color: #ff6b6b; }
    
    /* 사이드바 박스 스타일 */
    .sb-box { 
        background-color: white; padding: 15px; border-radius: 12px; 
        border: 1px solid #ffe3e3; margin-bottom: 15px; font-size: 0.9rem;
    }
    .stButton>button { width: 100%; background-color: #ff6b6b; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. 세션 상태 관리 (챗봇 대화 내용 보존)
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "안녕, 이레 엄마! 오늘 하루는 어땠어? 몸 상태는 좀 어때? 궁금한 게 있거나 위로가 필요하면 언제든 말해줘. ❤️"
    }]
if "todo" not in st.session_state: st.session_state.todo = {"영양제": False, "물 2L": False, "엽산": False}

# 3. 사이드바: 기록 및 체크리스트 (보조 기능)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🌿 이레네 집</h2>", unsafe_allow_html=True)
    
    # D-Day 및 예정일
    base_date = datetime(2026, 4, 9) # 아내분의 실제 날짜로 조정하세요
    due_date = base_date + timedelta(days=280)
    d_day = (due_date - datetime.now().date()).days
    st.markdown(f"""
        <div class="sb-box" style="text-align:center;">
            <b style="color:#ff6b6b;">이레를 만나는 날</b><br>
            <span style="font-size:1.5rem; font-weight:800; color:#ff4757;">D-{d_day}</span><br>
            <small>예정일: {due_date.strftime('%Y-%m-%d')}</small>
        </div>
    """, unsafe_allow_html=True)

    # 루틴 체크리스트
    with st.expander("✅ 오늘의 루틴 체크", expanded=True):
        st.session_state.todo["영양제"] = st.checkbox("영양제 복용", value=st.session_state.todo["영양제"])
        st.session_state.todo["물 2L"] = st.checkbox("수분 섭취", value=st.session_state.todo["물 2L"])
        st.session_state.todo["엽산"] = st.checkbox("엽산 챙기기", value=st.session_state.todo["엽산"])

    # 엄마 컨디션 기록
    with st.expander("🌡️ 컨디션 기록"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], label_visibility="collapsed")
        note = st.text_input("메모", placeholder="간단한 상태 기록")
        if st.button("기록 저장"):
            st.toast("기록 완료! 아빠가 확인할게요. 🥰")

    st.divider()
    # 마더세이프 버튼
    st.markdown(f'<a href="tel:1588-7309" style="text-decoration:none; background:#ff6b6b; color:white; padding:10px; border-radius:10px; display:block; text-align:center; font-weight:bold;">📞 마더세이프 상담</a>', unsafe_allow_html=True)

# 4. 메인 화면: 안심 챗봇 (핵심 기능)
st.markdown("<div class='main-header'><h1>💖 이레 안심 챗봇</h1><p>세계 최고 산부인과 전문의와 다정한 아빠가 함께해요</p></div>", unsafe_allow_html=True)

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 챗봇 로직 (OpenAI 연결)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("이레랑 엄마, 무엇이 궁금한가요?"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 답변 생성
    with st.chat_message("assistant"):
        # 페르소나 및 지침 주입
        system_msg = {
            "role": "system", 
            "content": """너는 '이레'의 아빠이자 세계 최고의 산부인과 전문의야. 
            1. 모든 의학 정보는 '마더세이프' 가이드를 최우선으로 하여 매우 정확하고 신중하게 제공해. 
            2. 어조는 항상 따뜻하고 부드러운 '해요체'를 사용해. 
            3. 답변 끝에는 반드시 아내(이레 엄마)를 향한 구체적인 응원과 사랑의 메시지를 포함해줘.
            4. 성경 구절(예: 시편 139:13, 이사야 49:15 등)을 인용해 영적 위로를 줘."""
        }
        
        full_messages = [system_msg] + st.session_state.messages
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=full_messages,
            temperature=0.7
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    
    st.session_state.messages.append({"role": "assistant", "content": msg})

# 5. 하단 탭 (참고 정보)
st.divider()
tab1, tab2 = st.tabs(["📅 임신 마일스톤", "👨‍🍳 아빠의 추천 레시피"])
with tab1:
    st.info("~12주: 보건소 등록 | 16주: 철분제 시작 | 24주: 임당 검사")
with tab2:
    st.success("오늘의 추천: 소고기 미역국 (단백질과 철분이 풍부해요!)")
