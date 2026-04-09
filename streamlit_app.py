import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json
import random

# 1. 페이지 설정
st.set_page_config(page_title="이레엄마를 위한 안심 가이드", page_icon="💖", layout="centered")

GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try:
        response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=10)
        return response.status_code == 200
    except:
        return False

# 2. CSS 보완 (사이드바 타이틀 중앙 정렬 및 입력창 레이아웃 수정)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fff5f7 !important;
        color: #333333 !important;
    }

    /* 사이드바 타이틀 중앙 정렬 */
    .sidebar-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ff6b6b;
        text-align: center;
        padding-top: 10px;
        padding-bottom: 5px;
        display: block;
        width: 100%;
    }

    /* 사이드바 오늘 날짜 스타일 */
    .sidebar-today {
        font-size: 0.9rem;
        font-weight: 500;
        color: #888888;
        text-align: center;
        margin-bottom: 15px;
        display: block;
        width: 100%;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #ffe8eb !important;
    }

    /* 입력창(Chat Input) 레이아웃 수정 */
    div[data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border-radius: 25px !important;
        padding: 8px 15px !important;
        border: 2px solid #ffe3e3 !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.08) !important;
        margin-bottom: 20px !important;
    }
    
    div[data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: #333333 !important;
        border: none !important;
        font-size: 1rem !important;
        -webkit-text-fill-color: #333333 !important;
    }

    .status-card { 
        background-color: #ffffff !important; padding: 25px; border-radius: 22px; 
        border-top: 6px solid #ff6b6b; 
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.1);
        margin-bottom: 25px;
    }

    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #ffe8eb !important;
        border-radius: 20px !important;
    }

    .bible-box { 
        background-color: #fff0f3 !important; padding: 20px; border-radius: 18px; 
        border-left: 6px solid #ff6b6b; margin-bottom: 25px; font-size: 0.95rem; 
    }
    
    .sb-box {
        background-color: #ffffff !important; border: 1px solid #ffe3e3; 
        border-radius: 18px; padding: 20px; text-align: center; margin-bottom: 15px;
    }

    .stButton>button { 
        width: 100%; background-color: #ff6b6b !important; color: #ffffff !important; 
        border-radius: 12px; height: 50px; font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로직 및 가이드 (기존과 동일)
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고 네가 배에서 나오기 전에 너를 성별하였고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("여인이 어찌 그 젖 먹는 자식을 잊겠으며... 나는 너를 잊지 아니할 것이라", "이사야 49:15"),
    ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라 여호와께서 네 오른쪽에서 네 그늘이 되시나니", "시편 121:5")
]

def get_comprehensive_guide(weeks):
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "엽산 복용을 시작하고 몸을 항상 따뜻하게 유지하세요.", "dad": "건강한 생활 습관을 함께 만들어가요.", "caution": "약물 복용 전 전문가와 상의하세요."},
        4: {"baby": "양귀비 씨앗 크기! 세포 분열이 활발해요.", "mom": "착상 시기이니 무리하지 말고 푹 쉬세요.", "dad": "임신 축하 꽃 한 송이로 마음을 전해보세요.", "caution": "대중교통 이용 시 가방 고리를 활용하세요."},
        8: {"baby": "라즈베리 크기! 심장 소리를 들을 수 있어요.", "mom": "입덧이 심할 수 있어요. 과일이나 차가운 음식이 도움돼요.", "dad": "집안 음식 냄새가 나지 않게 환기를 신경 써주세요.", "caution": "심한 복통이나 출혈 시 즉시 병원 방문!"},
        12: {"baby": "라임 크기! 이제 사람의 모습을 갖췄어요.", "mom": "기형아 검사 시기입니다. 마음을 편하게 가지세요.", "dad": "검진 날 동행해서 아기의 첫 움직임을 함께 보세요.", "caution": "감기약 복용 주의!"}
    }
    current = max([w for w in guides.keys() if w <= weeks] + [0])
    return guides[current]

# 4. 사이드바 (날짜 및 요일 추가)
with st.sidebar:
    # 타이틀 중앙 정렬
    st.markdown('<span class="sidebar-title">💖 이레 엄마 가이드</span>', unsafe_allow_html=True)
    
    # [추가] 오늘 날짜 표시 (예: 2026년 4월 9일 목요일)
    weekday_map = ['월', '화', '수', '목', '금', '토', '일']
    now = datetime.now()
    today_str = now.strftime("%Y년 %m월 %d일")
    weekday_str = weekday_map[now.weekday()]
    st.markdown(f'<span class="sidebar-today">{today_str} ({weekday_str})</span>', unsafe_allow_html=True)
    
    # 성경 구절
    random.seed(datetime.now().strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f'<div class="bible-box">"{verse}"<span class="bible-ref">- {ref} -</span></div>', unsafe_allow_html=True)

    # 날짜 입력 및 주수 계산
    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9).date())
    due_date = lmp_date + timedelta(days=280)
    today_date = now.date()
    total_days = max(0, (today_date - lmp_date).days)
    current_weeks, current_days = total_days // 7, total_days % 7
    d_day = (due_date - today_date).days

    st.markdown(f"""
        <div class="sb-box">
            <span style="font-size:0.95rem; color:#888;">우리 이레는 지금</span><br>
            <span style="font-size:1.8rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br>
            <b style="color:#ff6b6b; font-size:1.3rem;">D-{d_day if d_day > 0 else 'Day!'}</b>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🌡️ 오늘 엄마 컨디션 기록"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], key="cs", label_visibility="collapsed")
        memo = st.text_input("메모", key="cm", placeholder="아빠에게 한마디")
        if st.button("기록 전송", key="bc"):
            if save_to_sheets("컨디션", memo, cond): st.toast("기록 완료! ❤️")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("이레에게...", key="la", placeholder="오늘의 기록을 남겨보세요")
        if st.button("편지 저장", key="bl"):
            if save_to_sheets("태교편지", letter): st.success("저장 완료! ❤️")

    st.divider()
    st.markdown("<div style='text-align:center; color:#ff6b6b; font-weight:800; font-size:1.1rem;'>📞 마더세이프<br>1588-7309</div>", unsafe_allow_html=True)

# 5. 메인 화면 및 챗봇 (기존 로직 유지)
st.markdown("<h2 style='text-align:center; color:#ff6b6b; margin-bottom:35px;'>💖 이레 안심 가이드</h2>", unsafe_allow_html=True)

guide = get_comprehensive_guide(current_weeks)
st.markdown(f"""
<div class="status-card">
    <div class="guide-header">👶 {current_weeks}주차 이레 상태</div>
    <div class="guide-content">{guide['baby']}<br><br><b>엄마 준비:</b> {guide['mom']}</div>
    <div class="caution-text">⚠️ {guide['caution']}</div>
</div>
<div class="status-card">
    <div class="guide-header">🙋‍♂️ 아빠의 역할</div>
    <div class="guide-content">이번 주 미션: <b>"{guide['dad']}"</b><br><br>이레 엄마, 오늘도 이레를 품어주느라 고생 많았어요. 사랑해요!</div>
</div>
""", unsafe_allow_html=True)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 오늘 기분은 어때요? 걱정되는 게 있다면 무엇이든 물어보세요. 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("증상을 물어보거나 대화를 나눠보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {"role": "system", "content": f"산부인과 전문의 이레 아빠야. 현재 {current_weeks}주차인 아내에게 다정하게 답해줘. 마더세이프 근거로 답변하고 사랑한다고 말해줘."}
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
