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
        background-color: #fff5f7 !important; color: #333333 !important;
    }
    .sidebar-title { font-size: 1.4rem; font-weight: 800; color: #ff6b6b; text-align: center; display: block; padding-top: 10px; }
    .sidebar-today { font-size: 0.9rem; font-weight: 500; color: #888888; text-align: center; margin-bottom: 15px; display: block; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #ffe8eb !important; }
    .bible-box { 
        background-color: #fff0f3 !important; padding: 20px; border-radius: 18px; 
        border-left: 6px solid #ff6b6b; margin-bottom: 25px;
        word-break: keep-all; line-height: 1.8; font-size: 0.92rem; color: #444444 !important;
    }
    .bible-ref { display: block; text-align: right; font-weight: bold; color: #ff6b6b; margin-top: 10px; }
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
    .sb-box { background-color: #ffffff !important; border: 1px solid #ffe3e3; border-radius: 15px; padding: 18px; text-align: center; margin-bottom: 15px; }
    .stButton>button { width: 100%; background-color: #ff6b6b !important; color: #ffffff !important; border-radius: 12px; height: 48px; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. 성경 구절 (31일 순환)
bible_list = [
    ("내가 너를 모태에 짓기 전에 너를 알았고...", "예레미야 1:5"),
    ("보라 자식들은 여호와의 기업이요...", "시편 127:3"),
    ("그가 너로 말미암아 기쁨을 이기지 못하시며...", "스바냐 3:17"),
    ("여호와는 너를 지키시는 이시라...", "시편 121:5"),
    ("주께서 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("평강의 주께서 친히 평강을 주시고...", "데살로니가후서 3:16"),
    ("아무 것도 염려하지 말고...", "빌립보서 4:6"),
    ("여호와는 네게 복을 주시고...", "민수기 6:24"),
    ("너는 마음을 다하여 여호와를 신뢰하고...", "잠언 3:5"),
    ("하나님이 우리에게 주신 것은 사랑과 절제하는 마음이니", "디모데후서 1:7"),
    ("두려워하지 말라 내가 너와 함께 함이라", "이사야 41:10"),
    ("내게 능력 주시는 자 안에서 내가 모든 것을 할 수 있느니라", "빌립보서 4:13"),
    ("강하고 담대하라 두려워하지 말라", "여호수아 1:9"),
    ("모든 것이 합력하여 선을 이루느니라", "로마서 8:28"),
    ("구하라 그리하면 너희에게 주실 것이요", "마태복음 7:7"),
    ("수고하고 무거운 짐 진 자들아 다 내게로 오라", "마태복음 11:28"),
    ("오직 여호와를 앙망하는 자는 새 힘을 얻으리니", "이사야 40:31"),
    ("여호와를 기뻐하는 것이 너희의 힘이니라", "느헤미야 8:10"),
    ("사람이 마음으로 자기의 길을 계획할지라도...", "잠언 16:9"),
    ("항상 기뻐하라 쉬지 말고 기도하라 범사에 감사하라", "데살로니가전서 5:16"),
    ("주의 말씀은 내 발에 등이요 내 길에 빛이니이다", "시편 119:105"),
    ("너희 중에 누구든지 지혜가 부족하거든 하나님께 구하라", "야고보서 1:5"),
    ("하나님은 우리의 피난처시요 힘이시니", "시편 46:1"),
    ("믿음은 바라는 것들의 실상이요", "히브리서 11:1"),
    ("사랑은 오래 참고 사랑은 온유하며...", "고린도전서 13:4"),
    ("너희는 세상의 빛이라", "마태복음 5:14"),
    ("나를 단련하신 후에는 내가 정금 같이 나오리라", "욥기 23:10"),
    ("눈물을 흘리며 씨를 뿌리는 자는 기쁨으로 거두리로다", "시편 126:5"),
    ("여호와는 나의 목자시니 내게 부족함이 없으리로다", "시편 23:1"),
    ("네 시작은 미약하였으나 네 나중은 심히 창대하리라", "욥기 8:7"),
    ("너는 마음에 새기고 네 자녀에게 부지런히 가르치며...", "신명기 6:6")
]

# 4. 주차별 가이드 로직
def get_comprehensive_guide(weeks):
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "엽산 복용을 시작하고 몸을 따뜻하게 하세요.", "dad": "함께 건강한 생활 습관을 만들고 금주를 실천해 주세요.", "caution": "약물 복용 전 전문가와 상의하세요."},
        4: {"baby": "양귀비 씨앗 크기! 세포 분열이 활발해요.", "mom": "착상 시기이니 푹 쉬세요.", "dad": "임신 축하 꽃 한 송이를 선물해 보세요.", "caution": "안정이 가장 중요합니다."},
        8: {"baby": "라즈베리 크기! 심장 소리를 들을 수 있어요.", "mom": "입덧이 심할 수 있어요. 과일이 도움돼요.", "dad": "음식 냄새를 차단해주고 환기를 신경 써주세요.", "caution": "출혈 시 즉시 병원 방문!"},
        12: {"baby": "라임 크기! 이제 사람의 모습을 갖췄어요.", "mom": "기형아 검사 시기입니다.", "dad": "검진 날 꼭 동행해 주세요.", "caution": "감기약 등 약물 주의!"}
    }
    current = max([w for w in guides.keys() if w <= weeks] + [0])
    return guides[current]

# 5. 사이드바 (날짜 고정 반영)
with st.sidebar:
    st.markdown('<span class="sidebar-title">💖 이레 엄마 가이드</span>', unsafe_allow_html=True)
    now = datetime.now()
    st.markdown(f'<span class="sidebar-today">{now.strftime("%Y년 %m월 %d일")} ({["월","화","수","목","금","토","일"][now.weekday()]})</span>', unsafe_allow_html=True)
    
    day_index = (now.day - 1) % len(bible_list)
    verse, ref = bible_list[day_index]
    st.markdown(f'<div class="bible-box">"{verse}"<span class="bible-ref">- {ref} -</span></div>', unsafe_allow_html=True)

    # [수정됨] 마지막 생리일 기본값을 2026년 3월 15일로 고정
    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 3, 15).date())
    
    due_date = lmp_date + timedelta(days=280)
    total_days = max(0, (now.date() - lmp_date).days)
    current_weeks, current_days = total_days // 7, total_days % 7
    d_day = (due_date - now.date()).days

    st.markdown(f'<div class="sb-box"><span style="color:#888;">우리 이레는 지금</span><br><span style="font-size:1.8rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br><b style="color:#ff6b6b; font-size:1.3rem;">D-{d_day if d_day > 0 else "Day!"}</b></div>', unsafe_allow_html=True)

    with st.expander("🌡️ 오늘 엄마 컨디션 기록"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], key="cs", label_visibility="collapsed")
        memo = st.text_input("메모", key="cm", placeholder="아빠에게 한마디")
        if st.button("기록 전송"):
            if save_to_sheets("컨디션", memo, cond): st.toast("기록 완료! ❤️")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("이레에게...", key="la", placeholder="오늘의 기록을 남겨보세요")
        if st.button("편지 저장"):
            if save_to_sheets("태교편지", letter): st.success("저장 완료! ❤️")

    st.divider()
    st.markdown("<div style='text-align:center; color:#ff6b6b; font-weight:800;'>📞 마더세이프 1588-7309</div>", unsafe_allow_html=True)

# 6. 메인 화면
st.markdown("<h2 style='text-align:center; color:#ff6b6b; margin-bottom:30px;'>💖 이레 안심 가이드</h2>", unsafe_allow_html=True)
guide = get_comprehensive_guide(current_weeks)
st.markdown(f'<div class="status-card"><div class="guide-header">👶 {current_weeks}주차 이레 상태</div><div class="guide-content">{guide["baby"]}<br><br><b>엄마 준비:</b> {guide["mom"]}</div><div style="color:#ff4757; font-weight:700; margin-top:10px;">⚠️ 주의사항: {guide["caution"]}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="status-card"><div class="guide-header">🙋‍♂️ 이레 아빠의 역할</div><div class="guide-content">이번 주 미션: <b>"{guide["dad"]}"</b><br><br>이레 엄마, 오늘도 고생 많았어요. 사랑해요!</div></div>', unsafe_allow_html=True)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차네. 오늘 기분은 어때? 무엇이든 물어봐요. 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("증상, 음식, 약물 등 무엇이든 물어보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {"role": "system", "content": f"산부인과 전문의 이레 아빠야. 아내({current_weeks}주차)에게 다정하게 답해줘. 먹거리 질문 시 ⭕, ❌, ⚠️로 답하고 사랑한다고 해줘."}
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
