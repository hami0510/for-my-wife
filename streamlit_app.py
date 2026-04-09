import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json

# 1. 설정 및 디자인 (레이아웃 최적화)
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
    
    /* 사이드바 요소 간격 */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.8rem !important; }
    .sb-box { background-color: white; padding: 15px; border-radius: 12px; border: 1px solid #ffe3e3; }
    
    /* 메인 카드 레이아웃 통일 */
    .info-container { display: flex; gap: 15px; margin-bottom: 20px; }
    .status-card { 
        flex: 1; background-color: white; padding: 20px; border-radius: 15px; 
        border-top: 5px solid #ff6b6b; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        min-height: 160px;
    }
    .guide-title { color: #ff6b6b; font-weight: 700; font-size: 1.1rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
    
    /* 마더세이프 텍스트 스타일 */
    .ms-text { color: #ff6b6b; font-weight: 800; font-size: 1.1rem; text-align: center; margin-top: 10px; }
    
    .stButton>button { width: 100%; background-color: #ff6b6b; color: white; border: none; border-radius: 8px; height: 40px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 주차별 데이터베이스
def get_weekly_info(weeks):
    data = {
        0: {"baby": "준비 중이에요", "mom": "임신 준비기! 몸을 따뜻하게 하세요.", "dad": "함께 건강한 생활 습관을 만들어요."},
        4: {"baby": "양귀비 씨앗만 해요", "mom": "착상 시기예요. 무리하지 마세요.", "dad": "축하 파티와 함께 아내를 꼭 안아주세요."},
        8: {"baby": "라즈베리 크기에요", "mom": "입덧이 심해질 수 있는 시기예요.", "dad": "음식 냄새 환기에 각별히 신경 써주세요."},
        12: {"baby": "라임만큼 자랐어요", "mom": "안정기 진입! 1차 검사가 있어요.", "dad": "검진 날 병원에 꼭 동행해 주세요."},
        16: {"baby": "아보카도 크기에요", "mom": "철분제 복용을 시작할 때예요.", "dad": "아내의 등을 자주 토닥여 주세요."},
    }
    closest_week = max([w for w in data.keys() if w <= weeks] + [0])
    return data[closest_week]

# 3. 사이드바 (날짜 및 기록)
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#ff6b6b; margin-bottom:0;'>🌿 이레네 집</h3>", unsafe_allow_html=True)
    
    # 날짜 입력 및 계산
    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9).date())
    due_date = lmp_date + timedelta(days=280)
    total_days = (datetime.now().date() - lmp_date).days
    current_weeks = max(0, total_days // 7)
    current_days = max(0, total_days % 7)
    d_day = (due_date - datetime.now().date()).days

    st.markdown(f"""
        <div class="sb-box" style="text-align:center;">
            <span style="font-size:0.9rem; color:gray;">우리 이레는 지금</span><br>
            <span style="font-size:1.6rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br>
            <b style="color:#ff6b6b;">D-{d_day}</b><br>
            <small style="color:#999;">예정일: {due_date.strftime('%Y-%m-%d')}</small>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🌡️ 오늘 엄마 컨디션"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], label_visibility="collapsed")
        memo = st.text_input("아빠 메모", placeholder="기록 남기기")
        if st.button("기록 전송"):
            save_to_sheets("컨디션", memo, cond)
            st.toast("저장 완료!")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("편지...", placeholder="이레에게 남길 기록")
        if st.button("저장"):
            save_to_sheets("태교편지", letter)
            st.success("저장됨!")

    st.divider()
    # 마더세이프 전화번호만 표시
    st.markdown("<div style='text-align:center; font-size:0.8rem; color:gray;'>임산부 약물/음식 상담</div>", unsafe_allow_html=True)
    st.markdown("<div class='ms-text'>📞 마더세이프<br>1588-7309</div>", unsafe_allow_html=True)

# 4. 메인 화면 (레이아웃 정렬)
st.markdown("<h2 style='text-align:center; color:#ff6b6b; margin-bottom:30px;'>💖 이레 안심 가이드</h2>", unsafe_allow_html=True)

info = get_weekly_info(current_weeks)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="status-card">
        <div class="guide-title">👶 지금 우리 이레는</div>
        <p style="font-size:1rem; line-height:1.6;">우리 이레는 현재 <b>{info['baby']}</b>!<br>엄마 뱃속에서 무럭무럭 자라고 있어요.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="status-card">
        <div class="guide-title">🙋‍♂️ 아빠의 이번 주 미션</div>
        <p style="font-size:1rem; line-height:1.6;">{info['dad']}</p>
    </div>
    """, unsafe_allow_html=True)

# 챗봇 영역
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차에 접어들었네. 오늘 컨디션은 어때? 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("이레랑 엄마, 궁금한 게 있나요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {"role": "system", "content": "너는 다정한 산부인과 전문의 아빠야. 마더세이프 근거로 답변하고 사랑의 메시지로 마무리해."}
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
