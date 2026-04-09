import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json

# 1. 설정 및 디자인
st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="wide")

GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try: requests.post(GAS_URL, data=json.dumps(data))
    except: pass

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Noto Sans KR', sans-serif; background-color: #fffafb; }
    .sb-box { background-color: white; padding: 15px; border-radius: 12px; border: 1px solid #ffe3e3; margin-bottom: 15px; }
    .status-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ff6b6b; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .guide-title { color: #ff6b6b; font-weight: 700; font-size: 1.2rem; margin-bottom: 10px; }
    .stButton>button { width: 100%; background-color: #ff6b6b; color: white; border: none; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 주차별 상세 데이터베이스
def get_weekly_info(weeks):
    data = {
        4: {"baby": "양귀비 씨앗만 해요", "mom": "생리가 멈추고 예민해질 수 있어요.", "dad": "축하 파티와 함께 아내를 꼭 안아주세요."},
        8: {"baby": "라즈베리 크기에요", "mom": "입덧이 심해질 수 있는 시기예요.", "dad": "음식 냄새가 나지 않게 환기를 잘 해주세요."},
        12: {"baby": "라임만큼 자랐어요", "mom": "안정기에 접어드는 중요한 시기예요.", "dad": "1차 기형아 검사, 아내 곁을 지켜주세요."},
        16: {"baby": "아보카도 크기에요", "mom": "철분제 복용을 시작해야 해요.", "dad": "아내의 배를 부드럽게 마사지 해주세요."},
        20: {"baby": "바나나만큼 길어요", "mom": "태동을 처음 느낄 수 있어요!", "dad": "이레에게 태담을 많이 들려주세요."},
        24: {"baby": "옥수수 크기에요", "mom": "배가 제법 나와 허리가 아플 수 있어요.", "dad": "아내의 발과 다리를 정성껏 주물러주세요."},
        28: {"baby": "가지는 크기에요", "mom": "숨이 차고 다리에 쥐가 날 수 있어요.", "dad": "압박 스타킹을 신겨주거나 산책을 도와주세요."},
        32: {"baby": "배추 크기에요", "mom": "분만 리허설과 출산 가방을 준비해요.", "dad": "카시트 설치와 병원 동선을 미리 체크하세요."},
    }
    # 해당 주차가 없으면 가장 가까운 과거 주차 정보 반환
    closest_week = max([w for w in data.keys() if w <= weeks] + [4])
    return data[closest_week]

# 3. 사이드바 (날짜 지정 및 기록)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🌿 이레네 집</h2>", unsafe_allow_html=True)
    
    # [날짜 지정 기능]
    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9).date())
    due_date = lmp_date + timedelta(days=280)
    today = datetime.now().date()
    
    # 주수 계산
    total_days = (today - lmp_date).days
    current_weeks = total_days // 7
    current_days = total_days % 7
    d_day = (due_date - today).days

    st.markdown(f"""
        <div class="sb-box" style="text-align:center;">
            <b style="color:#ff6b6b;">이레는 지금</b><br>
            <span style="font-size:1.5rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br>
            <small>만나는 날까지 D-{d_day}</small><br>
            <small style="color:gray;">예정일: {due_date.strftime('%Y년 %m월 %d일')}</small>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🌡️ 오늘 엄마 컨디션"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], label_visibility="collapsed")
        memo = st.text_input("아빠에게 메모", placeholder="입덧이 심해")
        if st.button("컨디션 전송"):
            save_to_sheets("컨디션", memo, cond)
            st.toast("저장 완료! ❤️")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("이레에게...", placeholder="나중에 이레가 읽으면 좋아할 거야.")
        if st.button("편지 저장"):
            save_to_sheets("태교편지", letter)
            st.success("저장되었습니다.")

    st.divider()
    st.markdown(f'<a href="tel:1588-7309" style="text-decoration:none; background:#ff6b6b; color:white; padding:10px; border-radius:10px; display:block; text-align:center; font-weight:bold;">📞 마더세이프 연결</a>', unsafe_allow_html=True)

# 4. 메인 화면 (주차별 가이드 및 챗봇)
st.markdown("<h1 style='text-align:center; color:#ff6b6b;'>💖 이레 안심 가이드</h1>", unsafe_allow_html=True)

# 주차별 정보 카드
info = get_weekly_info(current_weeks)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="status-card">
        <div class="guide-title">👶 지금 우리 이레는</div>
        <p style="font-size:1.1rem;">우리 이레는 현재 <b>{info['baby']}</b>!<br>엄마 뱃속에서 열심히 자라는 중이에요.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="status-card" style="border-left-color: #fab005;">
        <div class="guide-title" style="color: #fab005;">🙋‍♂️ 아빠의 이번 주 미션</div>
        <p style="font-size:1.1rem;">{info['dad']}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 안심 챗봇 영역
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차에 접어들었네. 몸 상태는 어때? 궁금한 게 있으면 물어봐줘! 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("무엇이 궁금한가요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {"role": "system", "content": "너는 다정한 산부인과 전문의 아빠야. 마더세이프 근거로 답변하고 사랑의 메시지로 마무리해줘."}
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
