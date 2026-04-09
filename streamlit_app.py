import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json
import random

# 1. 설정 및 디자인 (라이트 모드 특화 디자인)
st.set_page_config(page_title="이레엄마를 위한 안심 가이드", page_icon="💖", layout="centered")

GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try:
        response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=10)
        return response.status_code == 200
    except:
        return False

# CSS: 라이트 모드에서 가장 예쁜 화이트 & 코랄 톤 고정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    /* 전체 배경: 아주 연한 핑크빛 화이트 */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #ffffff !important;
        color: #333333 !important;
    }

    /* 사이드바 스타일: 깨끗한 화이트 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #f0f0f0;
    }
    
    /* 사이드바 화살표 버튼 */
    [data-testid="stSidebarCollapsedControl"] svg, button[kind="header"] svg {
        fill: #ff6b6b !important; color: #ff6b6b !important;
    }

    /* 메인 카드 스타일: 부드러운 그림자와 핑크 포인트 */
    .status-card { 
        background-color: #ffffff !important; padding: 22px; border-radius: 18px; 
        border: 1px solid #fff0f0;
        border-top: 6px solid #ff6b6b; 
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.08);
        margin-bottom: 20px; color: #333333 !important;
    }
    .guide-header { color: #ff6b6b !important; font-weight: 700; font-size: 1.15rem; margin-bottom: 10px; }
    .guide-content { font-size: 0.98rem; line-height: 1.7; color: #444444 !important; }
    .caution-text { color: #ff4757 !important; font-weight: 600; margin-top: 8px; font-size: 0.9rem; }

    /* 챗봇 대화창: 깨끗한 라운드 스타일 */
    [data-testid="stChatMessage"] {
        background-color: #fdfdfd !important;
        color: #333333 !important;
        border: 1px solid #f5f5f5 !important;
        border-radius: 18px !important;
        margin-bottom: 12px;
    }
    
    /* 입력창(Chat Input): 핑크 테두리 강조 */
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 2px solid #ffeded !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
    div[data-testid="stChatInput"]:focus-within textarea {
        border-color: #ff6b6b !important;
    }

    /* 성경 구절 및 정보 박스 */
    .bible-box { 
        background-color: #fff8f8 !important; padding: 18px; border-radius: 15px; 
        border-left: 5px solid #ff6b6b; margin-bottom: 20px; font-size: 0.92rem; 
        color: #555555 !important; line-height: 1.6; font-style: italic;
    }
    .bible-ref { font-weight: bold; color: #ff6b6b !important; display: block; margin-top: 8px; text-align: right; font-style: normal; }
    
    .sb-box {
        background-color: #ffffff !important; border: 1px solid #ffe3e3; 
        border-radius: 15px; padding: 18px; text-align: center; margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(255,107,107,0.05);
    }

    /* 버튼 스타일 */
    .stButton>button { 
        width: 100%; background-color: #ff6b6b !important; color: #ffffff !important; 
        border: none; border-radius: 10px; height: 45px; font-weight: 700;
        transition: 0.3s;
    }
    
    /* 마더세이프 텍스트 */
    .ms-footer { text-align: center; color: #ff6b6b !important; font-weight: 800; font-size: 1.1rem; margin-top: 20px; }

    @media (max-width: 640px) {
        h2 { font-size: 1.35rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 및 로직
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고 네가 배에서 나오기 전에 너를 성별하였고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("여인이 어찌 그 젖 먹는 자식을 잊겠으며... 나는 너를 잊지 아니할 것이라", "이사야 49:15"),
    ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라 여호와께서 네 오른쪽에서 네 그늘이 되시나니", "시편 121:5")
]

def get_comprehensive_guide(weeks):
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "엽산 복용을 시작하고 몸을 항상 따뜻하게 유지하세요.", "dad": "함께 건강한 생활 습관을 만들어가요.", "caution": "약물 복용 전 반드시 전문가와 상의하세요."},
        4: {"baby": "양귀비 씨앗 크기! 세포 분열이 아주 활발해요.", "mom": "착상 시기이니 무리한 운동은 피하고 푹 쉬세요.", "dad": "임신 축하 꽃 한 송이로 감동을 선물해 보세요.", "caution": "대중교통 이용 시 가방 고리를 활용해 배려받으세요."},
        8: {"baby": "라즈베리 크기! 심장 소리를 들을 수 있어요.", "mom": "입덧이 심할 수 있어요. 차가운 음식이나 과일이 도움이 돼요.", "dad": "집안 음식 냄새가 나지 않게 환기를 잘 해주세요.", "caution": "심한 복통이나 출혈 시 즉시 병원을 방문하세요."},
        12: {"baby": "라임 크기! 이제 제법 사람의 모습을 갖췄어요.", "mom": "기형아 검사 시기입니다. 마음을 편안하게 가지세요.", "dad": "검진 날 꼭 동행해서 아기의 첫 움직임을 함께 보세요.", "caution": "기초 체온이 높아 감기로 오해할 수 있으니 약 주의!"}
    }
    current = max([w for w in guides.keys() if w <= weeks] + [0])
    return guides[current]

# 3. 사이드바 구성
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#ff6b6b; margin-top:0;'>💖 이레 엄마 가이드</h3>", unsafe_allow_html=True)
    
    # 오늘의 성경 구절
    random.seed(datetime.now().strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f'<div class="bible-box">"{verse}"<span class="bible-ref">- {ref} -</span></div>', unsafe_allow_html=True)

    # 날짜 및 주수 계산
    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9).date())
    due_date = lmp_date + timedelta(days=280)
    today = datetime.now().date()
    total_days = max(0, (today - lmp_date).days)
    current_weeks, current_days = total_days // 7, total_days % 7
    d_day = (due_date - today).days

    st.markdown(f"""
        <div class="sb-box">
            <span style="font-size:0.9rem; color:#888;">우리 이레는 지금</span><br>
            <span style="font-size:1.7rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br>
            <b style="color:#ff6b6b; font-size:1.2rem;">D-{d_day if d_day > 0 else 'Day!'}</b><br>
            <small style="color:#bbb;">예정일: {due_date.strftime('%Y-%m-%d')}</small>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🌡️ 오늘 엄마 컨디션 기록"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], key="cs", label_visibility="collapsed")
        memo = st.text_input("아빠에게 남길 메모", key="cm")
        if st.button("기록 전송", key="bc"):
            if save_to_sheets("컨디션", memo, cond): st.toast("기록 완료! ❤️")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("이레에게 남길 기록...", key="la")
        if st.button("편지 저장", key="bl"):
            if save_to_sheets("태교편지", letter): st.success("소중히 저장되었습니다! ❤️")

    st.divider()
    st.markdown("<div class='ms-footer'>📞 마더세이프<br>1588-7309</div>", unsafe_allow_html=True)

# 4. 메인 화면
st.markdown("<h2 style='text-align:center; color:#ff6b6b; margin-bottom:30px;'>💖 이레 안심 가이드</h2>", unsafe_allow_html=True)

guide = get_comprehensive_guide(current_weeks)
st.markdown(f"""
<div class="status-card">
    <div class="guide-header">👶 {current_weeks}주차 이레 상태</div>
    <div class="guide-content">
        {guide['baby']}<br><br>
        <b>엄마 준비:</b> {guide['mom']}
    </div>
    <div class="caution-text">⚠️ {guide['caution']}</div>
</div>
<div class="status-card">
    <div class="guide-header">🙋‍♂️ 이레 아빠의 역할</div>
    <div class="guide-content">이번 주 아빠의 미션: <b>"{guide['dad']}"</b></div>
</div>
""", unsafe_allow_html=True)

st.divider()

# 챗봇 영역
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차에 접어들었네. 오늘 몸 상태는 어때? 궁금한 게 있으면 무엇이든 물어봐. 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("증상을 물어보거나 대화를 나눠보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {"role": "system", "content": f"산부인과 전문의 이레 아빠야. 현재 {current_weeks}주차인 아내에게 다정하게 답해줘. 마더세이프 근거로 답변하고 사랑한다고 해줘."}
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
