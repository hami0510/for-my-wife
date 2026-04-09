import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json
import random

# 1. 설정 및 디자인 (사이드바 버튼 시인성 강화)
st.set_page_config(page_title="이레엄마를 위한 안심 가이드", page_icon="💖", layout="centered")

GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try:
        response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=10)
        return response.status_code == 200
    except:
        return False

# CSS: 사이드바 열기/닫기 화살표 버튼 색상 강제 고정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    /* 1. 전체 배경 및 기본 글자색 고정 */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fffafb !important;
        color: #222222 !important;
    }

    /* 2. ★ 사이드바 화살표 버튼(열기/닫기) 색상 고정 ★ */
    [data-testid="stSidebarCollapsedControl"] svg, 
    button[kind="header"] svg {
        fill: #ff6b6b !important;
        color: #ff6b6b !important;
        width: 30px !important;
        height: 30px !important;
    }
    
    /* 사이드바가 닫혀있을 때 나타나는 아이콘 배경 */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: rgba(255, 107, 107, 0.1) !important;
        border-radius: 0 10px 10px 0 !important;
    }

    /* 3. 사이드바 내부 요소 고정 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #f8f9fa !important;
        color: #222222 !important;
        border: 1px solid #ffe3e3 !important;
    }

    /* 4. 메인 화면 카드 및 챗봇 스타일 */
    .status-card { 
        background-color: #ffffff !important; padding: 22px; border-radius: 15px; 
        border-top: 5px solid #ff6b6b; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px; color: #222222 !important;
    }
    .guide-header { color: #ff6b6b !important; font-weight: 700; font-size: 1.15rem; margin-bottom: 12px; }
    .guide-content { font-size: 0.95rem; line-height: 1.7; color: #444444 !important; }
    
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        color: #222222 !important;
        border: 1px solid #ffe3e3 !important;
    }

    /* 5. 입력창(Chat Input) 색상 고정 */
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #222222 !important;
        border: 1px solid #ff6b6b !important;
        -webkit-text-fill-color: #222222 !important;
    }

    /* 6. 성경 구절 및 기타 박스 */
    .bible-box { 
        background-color: #fff5f5 !important; padding: 15px; border-radius: 12px; border-left: 4px solid #ff6b6b;
        margin-bottom: 15px; font-size: 0.92rem; color: #444444 !important;
    }
    .bible-ref { font-weight: bold; color: #ff6b6b !important; display: block; margin-top: 5px; text-align: right; }
    
    .stButton>button { width: 100%; background-color: #ff6b6b !important; color: #ffffff !important; border: none; border-radius: 8px; font-weight: 600; }

    @media (max-width: 640px) {
        .status-card { padding: 18px; }
        h2 { font-size: 1.3rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터베이스 및 기능 (기존과 동일)
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고 네가 배에서 나오기 전에 너를 성별하였고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("여인이 어찌 그 젖 먹는 자식을 잊겠으며... 나는 너를 잊지 아니할 것이라", "이사야 49:15"),
    ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라 여호와께서 네 오른쪽에서 네 그늘이 되시나니", "시편 121:5")
]

def get_comprehensive_guide(weeks):
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "엽산 복용을 시작하고 몸을 따뜻하게 하세요.", "dad": "건강한 생활 습관을 함께 만들어요.", "caution": "약물 복용 주의!"},
        4: {"baby": "양귀비 씨앗 크기!", "mom": "안정이 제일 중요해요.", "dad": "아내를 많이 안아주세요.", "caution": "대중교통 이용 시 배려받으세요."},
        8: {"baby": "라즈베리 크기!", "mom": "입덧이 심할 수 있어요.", "dad": "음식 냄새를 차단해 주세요.", "caution": "심한 복통 시 병원 방문!"},
        12: {"baby": "라임 크기!", "mom": "안정기에 접어듭니다.", "dad": "검진 날 꼭 동행해 주세요.", "caution": "기초 체온 변화 주의!"}
    }
    current = max([w for w in guides.keys() if w <= weeks] + [0])
    return guides[current]

# 3. 사이드바
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#ff6b6b;'>💖 이레 엄마 가이드</h3>", unsafe_allow_html=True)
    
    random.seed(datetime.now().strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f'<div class="bible-box">"{verse}"<span class="bible-ref">- {ref} -</span></div>', unsafe_allow_html=True)

    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9).date())
    due_date = lmp_date + timedelta(days=280)
    today = datetime.now().date()
    total_days = max(0, (today - lmp_date).days)
    current_weeks, current_days = total_days // 7, total_days % 7
    d_day = (due_date - today).days

    st.markdown(f"""
        <div class="sb-box" style="text-align:center; background-color:#ffffff !important; border: 1px solid #ffe3e3; border-radius:12px; padding:15px; margin-bottom:10px;">
            <span style="font-size:0.85rem; color:gray;">이레는 지금</span><br>
            <span style="font-size:1.6rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br>
            <b style="color:#ff6b6b; font-size:1.1rem;">D-{d_day if d_day > 0 else 'Day!'}</b>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🌡️ 오늘 엄마 컨디션 기록"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], key="cs", label_visibility="collapsed")
        memo = st.text_input("메모", key="cm")
        if st.button("구글 시트 전송", key="bc"):
            if save_to_sheets("컨디션", memo, cond): st.toast("기록 완료! ❤️")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("이레에게...", key="la")
        if st.button("기록 저장", key="bl"):
            if save_to_sheets("태교편지", letter): st.success("저장 완료! ❤️")

    st.divider()
    st.markdown("<div style='text-align:center; color:#ff6b6b; font-weight:800;'>📞 마더세이프<br>1588-7309</div>", unsafe_allow_html=True)

# 4. 메인 화면
st.markdown("<h2 style='text-align:center; color:#ff6b6b;'>💖 이레 안심 가이드</h2>", unsafe_allow_html=True)

guide = get_comprehensive_guide(current_weeks)
st.markdown(f"""
<div class="status-card">
    <div class="guide-header">👶 {current_weeks}주차 이레 상태</div>
    <div class="guide-content">{guide['baby']}<br><b>엄마 준비:</b> {guide['mom']}</div>
    <div class="caution-text">⚠️ {guide['caution']}</div>
</div>
<div class="status-card">
    <div class="guide-header">🙋‍♂️ 아빠의 역할</div>
    <div class="guide-content">이번 주 미션: <b>"{guide['dad']}"</b></div>
</div>
""", unsafe_allow_html=True)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
