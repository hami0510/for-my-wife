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

# 2. CSS: UI 최적화
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
    
    /* 카드 디자인 */
    .status-card { 
        background-color: #ffffff !important; padding: 22px; border-radius: 20px; 
        border-top: 6px solid #ff6b6b; box-shadow: 0 10px 25px rgba(255, 107, 107, 0.12);
        margin-bottom: 22px;
    }
    .guide-header { color: #ff6b6b !important; font-weight: 700; font-size: 1.2rem; margin-bottom: 12px; }
    .guide-content { font-size: 1rem; line-height: 1.8; color: #444444 !important; }

    /* 입력창 */
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

# 3. 데이터 및 가이드 로직 (아빠 미션 데이터 포함)
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요...", "시편 127:3"),
    ("여인이 어찌 그 젖 먹는 자식을 잊겠으며...", "이사야 49:15"),
    ("주께서 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라...", "시편 121:5")
]

def get_comprehensive_guide(weeks):
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "엽산 복용을 시작하고 몸을 따뜻하게 하세요.", "dad": "함께 건강한 생활 습관을 만들고, 금주를 실천해 주세요.", "caution": "약물 복용 전 반드시 전문가와 상의하세요."},
        4: {"baby": "양귀비 씨앗 크기! 세포 분열이 활발해요.", "mom": "착상 시기이니 무리하지 말고 푹 쉬세요.", "dad": "임신 축하 꽃 한 송이와 따뜻한 축하 인사를 건네보세요.", "caution": "대중교통 이용 시 가방 고리를 활용해 배려받으세요."},
        8: {"baby": "라즈베리 크기! 심장 소리를 들을 수 있어요.", "mom": "입덧이 가장 심할 시기예요. 과일이나 차가운 음식이 도움돼요.", "dad": "음식 냄새를 차단해주고, 아내가 먹고 싶어 하는 것을 바로 구해주세요.", "caution": "심한 복통이나 출혈 시 즉시 병원 방문!"},
        12: {"baby": "라임 크기! 이제 제법 사람의 모습을 갖췄어요.", "mom": "기형아 검사 시기입니다. 마음을 편하게 가지세요.", "dad": "검진 날 꼭 동행해서 아기의 첫 움직임을 함께 보세요.", "caution": "감기약 등 약물 복용 주의!"},
        16: {"baby": "아보카도 크기! 뼈가 단단해지고 소리를 들어요.", "mom": "철분제 복용 시작! 수분 섭취를 늘려 변비를 예방하세요.", "dad": "아내의 배에 귀를 대고 이레에게 아빠 목소리를 들려주세요.", "caution": "기립성 저혈압(어지럼증)을 조심하세요."},
        20: {"baby": "바나나 길이! 태동이 느껴지기 시작해요.", "mom": "체중이 늘어 허리가 아플 수 있어요. 가벼운 산책을 권해요.", "dad": "태동이 느껴질 때 같이 손을 얹어 이레와 교감해 주세요.", "caution": "무거운 물건을 드는 것은 피해야 합니다."},
        24: {"baby": "옥수수 크기! 임당 검사가 있는 주예요.", "mom": "단 음식 섭취를 조절하고 산책을 생활화하세요.", "dad": "부종이 심해질 수 있으니 자기 전 다리 마사지를 꼭 해주세요.", "caution": "배 뭉침이 잦다면 즉시 휴식을 취하세요."}
    }
    current = max([w for w in guides.keys() if w <= weeks] + [0])
    return guides[current]

# 4. 사이드바
with st.sidebar:
    st.markdown('<span class="sidebar-title">💖 이레 엄마 가이드</span>', unsafe_allow_html=True)
    now = datetime.now()
    st.markdown(f'<span class="sidebar-today">{now.strftime("%Y년 %m월 %d일")} ({["월","화","수","목","금","토","일"][now.weekday()]})</span>', unsafe_allow_html=True)
    
    random.seed(now.strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f'<div class="bible-box">"{verse}"<br><span style="display:block; text-align:right; font-weight:bold; color:#ff6b6b;">- {ref} -</span></div>', unsafe_allow_html=True)

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

# 5. 메인 화면 (아빠 역할 카드 복구)
st.markdown("<h2 style='text-align:center; color:#ff6b6b; margin-bottom:30px;'>💖 이레 안심 가이드</h2>", unsafe_allow_html=True)

guide = get_comprehensive_guide(current_weeks)

# 주차별 상태 가이드 카드
st.markdown(f"""
<div class="status-card">
    <div class="guide-header">👶 {current_weeks}주차 이레 상태</div>
    <div class="guide-content">
        {guide['baby']}<br><br>
        <b>엄마 준비:</b> {guide['mom']}
    </div>
    <div style="color:#ff4757; font-weight:700; margin-top:10px;">⚠️ 주의사항: {guide['caution']}</div>
</div>
""", unsafe_allow_html=True)

# [복구된 부분] 아빠의 역할 카드
st.markdown(f"""
<div class="status-card">
    <div class="guide-header">🙋‍♂️ 이레 아빠의 역할</div>
    <div class="guide-content">
        이번 주 아빠가 해줘야 할 미션: <b>"{guide['dad']}"</b><br><br>
        이레 엄마, 오늘도 이레를 품어주느라 정말 고생 많았어요. 아빠가 항상 곁에서 응원할게요. 사랑해요!
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# 채팅 인터페이스
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차네. 오늘 컨디션은 어때? 무엇이든 물어봐. 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("음식, 음료, 약물 등 무엇이든 물어보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {
            "role": "system", 
            "content": f"""너는 산부인과 전문의이자 이레 아빠야. 아내({current_weeks}주차)에게 답할 때 다음 규칙을 지켜줘:
            1. [음식/음료/약물 검수] 절대 금지는 [❌ 절대 금지]로 강력 경고하고 대체품 추천. 주의는 [⚠️ 주의]로 적정량 안내.
            2. 마더세이프(MotherSafe) 기반으로 정확하게 답할 것.
            3. 항상 다정하게 말하고 마지막엔 "사랑해"라고 할 것."""
        }
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
