import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="wide")

# [보안 팁] 나중에 Streamlit Secrets에 "GAS_URL"이라는 이름으로 숨겨두시면 더 안전해요!
GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    """구글 앱스 스크립트를 통해 시트에 데이터 전송"""
    data = {
        "type": type_val,
        "content": content,
        "status": status
    }
    try:
        # 비동기 전송으로 앱 속도 유지
        requests.post(GAS_URL, data=json.dumps(data))
    except:
        pass

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #fffafb; 
    }
    .sb-box { background-color: white; padding: 15px; border-radius: 12px; border: 1px solid #ffe3e3; margin-bottom: 15px; }
    .main-header { text-align: center; color: #ff6b6b; padding: 10px; }
    .stButton>button { width: 100%; background-color: #ff6b6b; color: white; border: none; border-radius: 8px; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕, 이레 엄마! 오늘 하루는 어땠어? 궁금한 게 있으면 무엇이든 물어봐요. 🥰"}]

# 3. 사이드바 구성 (기록 및 대시보드)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🌿 이레네 집</h2>", unsafe_allow_html=True)
    
    # D-Day 계산 (오류 방지 date 통일)
    base_date = datetime(2026, 4, 9).date()
    due_date = base_date + timedelta(days=280)
    d_day = (due_date - datetime.now().date()).days
    
    st.markdown(f"""
        <div class="sb-box" style="text-align:center;">
            <b style="color:#ff6b6b;">이레를 만나는 날</b><br>
            <span style="font-size:1.8rem; font-weight:800; color:#ff4757;">D-{d_day if d_day > 0 else 'Day!'}</span><br>
            <small>예정일: {due_date.strftime('%Y년 %m월 %d일')}</small>
        </div>
    """, unsafe_allow_html=True)

    # 기능 1: 컨디션 기록
    with st.expander("🌡️ 오늘 엄마 컨디션"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], label_visibility="collapsed")
        memo = st.text_input("아빠에게 남길 메모", placeholder="예: 입덧이 심해")
        if st.button("컨디션 전송"):
            save_to_sheets("컨디션", memo, cond)
            st.toast("아빠 시트에 저장되었어요! ❤️")

    # 기능 2: 태교 편지함
    with st.expander("💌 이레에게 쓰는 편지"):
        letter = st.text_area("오늘의 기록...", placeholder="나중에 이레가 읽으면 정말 좋아할 거야.")
        if st.button("편지 저장"):
            save_to_sheets("태교편지", letter)
            st.success("소중한 기록이 저장되었습니다.")

    st.divider()
    st.markdown(f'<a href="tel:1588-7309" style="text-decoration:none; background:#ff6b6b; color:white; padding:12px; border-radius:10px; display:block; text-align:center; font-weight:bold;">📞 마더세이프 상담 연결</a>', unsafe_allow_html=True)

# 4. 메인 화면 (안심 챗봇)
st.markdown("<div class='main-header'><h1>💖 이레 안심 가이드</h1><p>아빠의 사랑과 의사의 전문성을 담은 대화</p></div>", unsafe_allow_html=True)

# 채팅 히스토리 출력
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# OpenAI API (st.secrets["OPENAI_API_KEY"]가 설정되어 있어야 합니다)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("이레랑 엄마, 무엇이 궁금한가요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 페르소나 주입
        sys_msg = {
            "role": "system", 
            "content": """너는 이레 아빠이자 세계 최고의 산부인과 전문의야. 
            다정한 해요체로 답변하고, 끝에는 항상 아내를 향한 응원 메시지를 남겨줘. 
            의학 정보는 마더세이프 가이드를 최우선으로 하고, 가끔 시편 121:5 같은 성경 구절로 위로해줘."""
        }
        
        full_context = [sys_msg] + st.session_state.messages
        response = client.chat.completions.create(model="gpt-4o", messages=full_context, temperature=0.7)
        msg = response.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})

# 5. 하단 정보 탭
st.divider()
tab1, tab2 = st.tabs(["📅 임신 마일스톤", "👨‍🍳 아빠의 추천 레시피"])
with tab1:
    st.info("~12주: 보건소 등록 | 16주: 철분제 시작 | 24주: 임당 검사")
with tab2:
    st.success("오늘의 메뉴: 소고기 미역국 (단백질과 철분이 풍부해요!)")
