import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json
import random

# 1. 설정 및 디자인 (테마 및 시인성 강화)
st.set_page_config(page_title="이레엄마를 위한 안심 가이드", page_icon="💖", layout="centered")

GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try:
        response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=10)
        return response.status_code == 200
    except:
        return False

# CSS: 다크모드 무시 및 모바일 시인성 고정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fffafb !important;
        color: #222222 !important;
    }
    [data-testid="stSidebarCollapsedControl"] svg, button[kind="header"] svg {
        fill: #ff6b6b !important; color: #ff6b6b !important; width: 30px !important; height: 30px !important;
    }
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #f8f9fa !important; color: #222222 !important; border: 1px solid #ffe3e3 !important;
    }
    .status-card { 
        background-color: #ffffff !important; padding: 20px; border-radius: 15px; 
        border-top: 5px solid #ff6b6b; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px; color: #222222 !important;
    }
    .guide-header { color: #ff6b6b !important; font-weight: 700; font-size: 1.1rem; margin-bottom: 10px; }
    .guide-content { font-size: 0.95rem; line-height: 1.6; color: #444444 !important; }
    [data-testid="stChatMessage"] { background-color: #ffffff !important; color: #222222 !important; border: 1px solid #ffe3e3 !important; }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span { color: #222222 !important; }
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important; color: #222222 !important; border: 1px solid #ff6b6b !important;
        -webkit-text-fill-color: #222222 !important;
    }
    .bible-box { background-color: #fff5f5 !important; padding: 15px; border-radius: 12px; border-left: 4px solid #ff6b6b; margin-bottom: 15px; font-size: 0.9rem; color: #444444 !important; }
    .bible-ref { font-weight: bold; color: #ff6b6b !important; display: block; margin-top: 5px; text-align: right; }
    .stButton>button { width: 100%; background-color: #ff6b6b !important; color: #ffffff !important; border: none; border-radius: 8px; font-weight: 600; }
    @media (max-width: 640px) { h2 { font-size: 1.3rem !important; } }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터베이스
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고 네가 배에서 나오기 전에 너를 성별하였고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("여인이 어찌 그 젖 먹는 자식을 잊겠으며... 나는 너를 잊지 아니할 것이라", "이사야 49:15"),
    ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라 여호와께서 네 오른쪽에서 네 그늘이 되시나니", "시편 121:5")
]

def get_comprehensive_guide(weeks):
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "엽산 복용을 시작하고 몸을 따뜻하게 하세요.", "dad": "함께 건강한 생활 습관을 만들어요.", "caution": "약물 복용 주의!"},
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
    total_days = max(0, (datetime.now().date() - lmp_date).days)
    current_weeks, current_days = total_days // 7, total_days % 7
    d_day = (due_date - datetime.now().date()).days

    st.markdown(f"""
        <div style="background-color:#ffffff; border:1px solid #ffe3e3; border-radius:12px; padding:15px; text-align:center; margin-bottom:10px;">
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
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차네. 오늘 컨디션은 어때? 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("증상을 물어보거나 대화를 나눠보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {"role": "system", "content": f"산부인과 전문의 이레 아빠야. 현재 {current_weeks}주차인 아내에게 다정하게 답해줘."}
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
