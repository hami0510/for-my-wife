import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json
import random

# 1. 페이지 설정
st.set_page_config(page_title="이레 엄마를 위한 안심 가이드", page_icon="💖", layout="centered")

# 구글 시트 연동 URL (제공해주신 URL 유지)
GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try:
        response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=10)
        return response.status_code == 200
    except:
        return False

# 2. CSS: 입력창 개선 및 테마 고도화
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    /* 전체 배경 */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fffafb !important;
    }

    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #ffe8eb !important;
    }

    /* 메인 카드 디자인 */
    .status-card { 
        background-color: #ffffff !important; padding: 22px; border-radius: 20px; 
        border-top: 6px solid #ff6b6b; 
        box-shadow: 0 10px 25px rgba(255, 107, 107, 0.1);
        margin-bottom: 22px;
    }
    .guide-header { color: #ff6b6b !important; font-weight: 700; font-size: 1.2rem; margin-bottom: 8px; }
    .guide-content { font-size: 1rem; line-height: 1.7; color: #444444 !important; }
    .caution-box { 
        background-color: #fff0f0; padding: 12px; border-radius: 10px; 
        color: #ff4757; font-weight: 600; font-size: 0.9rem; margin-top: 10px;
    }

    /* 🔥 핵심 개선: 입력창(Chat Input) 커스텀 */
    div[data-testid="stChatInput"] {
        padding: 1rem 0 !important;
    }
    div[data-testid="stChatInput"] textarea {
        border: 2px solid #ff6b6b !important;
        border-radius: 15px !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        font-size: 16px !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #ff6b6b !important;
    }

    /* 성경 구절 및 기타 박스 */
    .bible-box { 
        background-color: #fff0f3 !important; padding: 18px; border-radius: 15px; 
        border-left: 5px solid #ff6b6b; margin-bottom: 15px; font-size: 0.9rem; 
        color: #555555; line-height: 1.6;
    }
    .bible-ref { font-weight: bold; color: #ff6b6b; display: block; margin-top: 5px; text-align: right; }
    
    /* 마더세이프 버튼 스타일 */
    .ms-button {
        display: block; width: 100%; padding: 12px; background-color: #ff6b6b;
        color: white !important; text-align: center; border-radius: 12px;
        text-decoration: none; font-weight: 700; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로직 (주차별 비유 추가 반영)
def get_baby_size_metaphor(weeks):
    metaphor = {
        1: "씨앗", 3: "좁쌀", 4: "양귀비 씨앗", 5: "사과 씨앗", 6: "완두콩", 
        7: "블루베리", 8: "라즈베리", 9: "체리", 10: "딸기", 11: "무화과", 12: "라임",
        16: "아보카도", 20: "바나나", 24: "옥수수"
    }
    return metaphor.get(weeks, "작고 소중한 생명")

def get_comprehensive_guide(weeks):
    # (기존 가이드 데이터 유지하되 보완)
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "엽산 복용을 시작하고 몸을 항상 따뜻하게 유지하세요.", "dad": "함께 건강한 생활 습관을 만들어가요.", "caution": "약물 복용 전 전문가와 상의하세요."},
        4: {"baby": "양귀비 씨앗 크기! 세포 분열이 활발해요.", "mom": "착상 시기이니 무리하지 말고 푹 쉬세요.", "dad": "임신 축하 꽃 한 송이로 마음을 전해보세요.", "caution": "대중교통 이용 시 가방 고리를 활용하세요."},
        8: {"baby": "라즈베리 크기! 심장 소리를 들을 수 있어요.", "mom": "입덧이 심할 수 있어요. 찬 음식이나 과일이 도움돼요.", "dad": "집안 음식 냄새가 나지 않게 환기를 신경 써주세요.", "caution": "심한 복통이나 출혈 시 즉시 병원 방문!"},
        12: {"baby": "라임 크기! 이제 사람의 모습을 갖췄어요.", "mom": "기형아 검사 시기입니다. 마음을 편하게 가지세요.", "dad": "검진 날 동행해서 아기의 첫 움직임을 함께 보세요.", "caution": "감기약 등 약물 복용 시 마더세이프 상담 필수!"},
        16: {"baby": "아보카도 크기! 뼈가 단단해지고 소리를 들어요.", "mom": "철분제 복용 시작! 수분 섭취를 늘리세요.", "dad": "아빠 목소리를 태담으로 자주 들려주세요.", "caution": "기립성 저혈압 주의! 천천히 일어나세요."},
        20: {"baby": "바나나 길이! 태동이 느껴지기 시작해요.", "mom": "배가 제법 나와 허리가 아플 수 있어요.", "dad": "태동이 느껴질 때 같이 손을 얹고 대화하세요.", "caution": "무리한 장거리 이동은 피하는 게 좋아요."},
        24: {"baby": "옥수수 크기! 임당 검사가 있는 주예요.", "mom": "단 음식 섭취를 줄이고 가벼운 산책을 하세요.", "dad": "아내의 발과 다리를 정성껏 마사지해 주세요.", "caution": "배 뭉침이 잦다면 즉시 휴식을 취하세요."}
    }
    current = max([w for w in guides.keys() if w <= weeks] + [0])
    return guides[current]

# 4. 사이드바 구성
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#ff6b6b;'>💖 이레 엄마 가이드</h3>", unsafe_allow_html=True)
    
    # 성경 구절
    bible_verses = [
        ("내가 너를 모태에 짓기 전에 너를 알았고...", "예레미야 1:5"),
        ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
        ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13")
    ]
    random.seed(datetime.now().strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f'<div class="bible-box">"{verse}"<span class="bible-ref">- {ref} -</span></div>', unsafe_allow_html=True)

    # 날짜 계산
    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9).date())
    due_date = lmp_date + timedelta(days=280)
    today = datetime.now().date()
    total_days = max(0, (today - lmp_date).days)
    current_weeks, current_days = total_days // 7, total_days % 7
    d_day = (due_date - today).days

    st.markdown(f"""
        <div style="background-color: white; border: 1px solid #ffe3e3; border-radius: 15px; padding: 15px; text-align: center;">
            <span style="font-size:0.8rem; color:#888;">우리 이레는 지금</span><br>
            <span style="font-size:1.5rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br>
            <b style="color:#ff6b6b;">예정일 D-{d_day if d_day > 0 else 'Day!'}</b>
        </div>
    """, unsafe_allow_html=True)

    # 기록 섹션
    with st.expander("🌡️ 오늘 엄마 컨디션"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"])
        memo = st.text_input("메모", placeholder="이레 아빠에게...")
        if st.button("기록 전송"):
            if save_to_sheets("컨디션", memo, cond): st.toast("기록 완료! ❤️")

    # 마더세이프 다이렉트 버튼
    st.markdown('<a href="tel:1588-7309" class="ms-button">📞 마더세이프 전화상담</a>', unsafe_allow_html=True)

# 5. 메인 화면
st.markdown("<h2 style='text-align:center; color:#ff6b6b;'>🌸 이레 안심 가이드 🌸</h2>", unsafe_allow_html=True)

guide = get_comprehensive_guide(current_weeks)
metaphor = get_baby_size_metaphor(current_weeks)

# 주차별 가이드 카드
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="status-card">
        <div class="guide-header">👶 이레는 지금</div>
        <div class="guide-content"><b>{metaphor}</b> 크기예요!<br>{guide['baby']}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="status-card">
        <div class="guide-header">🙋‍♂️ 아빠 미션</div>
        <div class="guide-content">{guide['dad']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="status-card">
    <div class="guide-header">👩 엄마를 위한 가이드</div>
    <div class="guide-content">{guide['mom']}</div>
    <div class="caution-box">⚠️ 주의사항: {guide['caution']}</div>
</div>
""", unsafe_allow_html=True)

# 6. 채팅 섹션
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차네요. 오늘 몸 상태는 좀 어때요? 걱정되는 게 있다면 무엇이든 물어보세요. 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# OpenAI API (st.secrets 사용 권장)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    if prompt := st.chat_input("증상을 물어보거나 대화를 나눠보세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            sys_msg = {
                "role": "system", 
                "content": f"너는 다정한 산부인과 전문의이자 남편이야. 아내는 임신 {current_weeks}주차야. 모든 답변은 마더세이프의 의학적 근거를 바탕으로 하되, 매우 따뜻하고 부드러운 '해요체'를 사용해줘. 답변 끝에는 반드시 아내를 격려하고 사랑한다는 메시지를 포함해줘."
            }
            res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
            msg = res.choices[0].message.content
            st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
except Exception as e:
    st.error("API 키를 확인해주세요. (st.secrets['OPENAI_API_KEY'])")
