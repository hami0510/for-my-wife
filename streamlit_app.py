import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json
import random

# 1. 페이지 설정 및 보안 설정
st.set_page_config(page_title="이레엄마를 위한 안심 가이드", page_icon="💖", layout="centered")

GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try:
        response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=10)
        return response.status_code == 200
    except:
        return False

# 2. CSS: 연분홍 테마, 중앙 정렬 타이틀, 모바일 최적화 입력창
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fff5f7 !important;
        color: #333333 !important;
    }

    .sidebar-title { font-size: 1.4rem; font-weight: 800; color: #ff6b6b; text-align: center; display: block; padding: 10px 0; }
    .sidebar-today { font-size: 0.9rem; font-weight: 500; color: #888888; text-align: center; margin-bottom: 15px; display: block; }

    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #ffe8eb !important; }
    [data-testid="stSidebarCollapsedControl"] svg, button[kind="header"] svg { fill: #ff6b6b !important; color: #ff6b6b !important; }

    .status-card { 
        background-color: #ffffff !important; padding: 22px; border-radius: 20px; 
        border-top: 6px solid #ff6b6b; box-shadow: 0 10px 25px rgba(255, 107, 107, 0.12);
        margin-bottom: 22px;
    }
    .guide-header { color: #ff6b6b !important; font-weight: 700; font-size: 1.2rem; margin-bottom: 12px; }
    .guide-content { font-size: 1rem; line-height: 1.8; color: #444444 !important; }

    div[data-testid="stChatInput"] {
        background-color: #ffffff !important; border-radius: 25px !important; 
        padding: 5px 15px !important; border: 2px solid #ffe3e3 !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.08) !important;
    }
    div[data-testid="stChatInput"] textarea { color: #333333 !important; -webkit-text-fill-color: #333333 !important; }

    .bible-box { background-color: #fff0f3 !important; padding: 18px; border-radius: 15px; border-left: 5px solid #ff6b6b; margin-bottom: 22px; }
    .sb-box { background-color: #ffffff !important; border: 1px solid #ffe3e3; border-radius: 15px; padding: 18px; text-align: center; margin-bottom: 15px; }
    .stButton>button { width: 100%; background-color: #ff6b6b !important; color: #ffffff !important; border-radius: 12px; height: 48px; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 및 가이드 로직
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("여인이 어찌 그 젖 먹는 자식을 잊겠으며...", "이사야 49:15"),
    ("주께서 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라...", "시편 121:5")
]

def get_comprehensive_guide(weeks):
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "엽산 복용을 시작하고 몸을 따뜻하게 하세요.", "dad": "함께 건강한 생활 습관을 만들어요.", "caution": "약물 복용 전 전문가와 상의하세요."},
        4: {"baby": "양귀비 씨앗 크기!", "mom": "착상 시기이니 푹 쉬세요.", "dad": "임신 축하 꽃 한 송이를 선물해 보세요.", "caution": "대중교통 이용 시 가방 고리를 활용하세요."},
        8: {"baby": "라즈베리 크기!", "mom": "입덧이 심할 수 있어요. 과일이 도움돼요.", "dad": "음식 냄새 차단 및 환기를 신경 써주세요.", "caution": "심한 복통이나 출혈 시 병원 방문!"},
        12: {"baby": "라임 크기!", "mom": "기형아 검사 시기입니다.", "dad": "검진 날 동행해서 아기를 함께 보세요.", "caution": "감기약 등 약물 복용 주의!"}
    }
    current = max([w for w in guides.keys() if w <= weeks] + [0])
    return guides[current]

# 4. 사이드바 (날짜 및 기록)
with st.sidebar:
    st.markdown('<span class="sidebar-title">💖 이레 엄마 가이드</span>', unsafe_allow_html=True)
    now = datetime.now()
    st.markdown(f'<span class="sidebar-today">{now.strftime("%Y년 %m월 %d일")} ({["월","화","수","목","금","토","일"][now.weekday()]})</span>', unsafe_allow_html=True)
    
    random.seed(now.strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f'<div class="bible-box">"{verse}"<span style="display:block; text-align:right; font-weight:bold; color:#ff6b6b;">- {ref} -</span></div>', unsafe_allow_html=True)

    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9).date())
    due_date = lmp_date + timedelta(days=280)
    total_days = max(0, (now.date() - lmp_date).days)
    current_weeks, current_days = total_days // 7, total_days % 7
    d_day = (due_date - now.date()).days

    st.markdown(f'<div class="sb-box"><span style="color:#888;">우리 이레는 지금</span><br><span style="font-size:1.8rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br><b style="color:#ff6b6b; font-size:1.3rem;">D-{d_day if d_day > 0 else "Day!"}</b></div>', unsafe_allow_html=True)

    with st.expander("🌡️ 오늘 엄마 컨디션 기록"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], key="cs", label_visibility="collapsed")
        memo = st.text_input("메모", key="cm")
        if st.button("기록 전송"):
            if save_to_sheets("컨디션", memo, cond): st.toast("기록 완료! ❤️")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("이레에게...", key="la")
        if st.button("편지 저장"):
            if save_to_sheets("태교편지", letter): st.success("저장 완료! ❤️")

    st.divider()
    st.markdown("<div style='text-align:center; color:#ff6b6b; font-weight:800;'>📞 마더세이프 1588-7309</div>", unsafe_allow_html=True)

# 5. 메인 및 챗봇 (먹거리 안전 로직 탑재)
st.markdown("<h2 style='text-align:center; color:#ff6b6b; margin-bottom:30px;'>💖 이레 안심 가이드</h2>", unsafe_allow_html=True)

guide = get_comprehensive_guide(current_weeks)
st.markdown(f'<div class="status-card"><div class="guide-header">👶 {current_weeks}주차 이레 상태</div><div class="guide-content">{guide["baby"]}<br><br><b>엄마 준비:</b> {guide["mom"]}</div><div style="color:#ff4757; font-weight:700; margin-top:10px;">⚠️ {guide["caution"]}</div></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차네. 오늘 먹고 싶은 거나 궁금한 음식, 약이 있니? 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("음식, 음료, 약물 등 무엇이든 물어보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {
            "role": "system", 
            "content": f"""너는 산부인과 전문의이자 이레 아빠야. 아내({current_weeks}주차)에게 답할 때 다음 규칙을 절대적으로 지켜줘:
            1. [음식/음료/약물 검수]
               - 술, 담배, 여드름약(이소트레티노인), 날것(회/육회), 살균안된 우유 등은 [❌ 절대 금지]라고 강력히 경고하고 절대 먹지 말라고 할 것.
               - 카페인, 참치캔, 맵고 짠 음식은 [⚠️ 주의]와 함께 적정량을 안내할 것.
               - 금지/주의 식품일 경우 반드시 다정한 말투로 '대체할 수 있는 맛있는 음식'을 추천할 것.
            2. [전문성] 마더세이프(MotherSafe) 가이드를 기반으로 정확하게 답할 것.
            3. [감정] 아내를 걱정하는 마음을 담아 다정하게 말하고 마지막엔 "사랑해"라고 할 것."""
        }
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
