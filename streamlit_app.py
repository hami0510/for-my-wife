import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import requests
import json
import random

# 1. 설정 및 디자인 (일관된 레이아웃 유지)
st.set_page_config(page_title="이레엄마를 위한 안심 가이드", page_icon="💖", layout="wide")

GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try:
        response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=10)
        return response.status_code == 200
    except:
        return False

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Noto Sans KR', sans-serif; background-color: #fffafb; }
    
    /* 사이드바 스타일 */
    .sb-box { background-color: white; padding: 15px; border-radius: 12px; border: 1px solid #ffe3e3; margin-bottom: 10px; }
    
    /* 성경 구절 박스 디자인 */
    .bible-box { 
        background-color: #fff5f5; padding: 15px; border-radius: 12px; border-left: 4px solid #ff6b6b;
        margin-bottom: 15px; font-size: 0.9rem; color: #444; line-height: 1.6;
        box-shadow: 0 2px 5px rgba(255,107,107,0.1);
    }
    .bible-ref { font-weight: bold; color: #ff6b6b; display: block; margin-top: 5px; text-align: right; }

    /* 메인 카드 스타일 */
    .status-card { 
        background-color: white; padding: 22px; border-radius: 15px; 
        border-top: 5px solid #ff6b6b; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        min-height: 220px;
    }
    .guide-header { color: #ff6b6b; font-weight: 700; font-size: 1.15rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    .guide-content { font-size: 0.95rem; line-height: 1.7; color: #444; }
    .caution-text { color: #e63946; font-weight: 600; margin-top: 10px; font-size: 0.9rem; }
    .ms-footer { text-align: center; color: #ff6b6b; font-weight: 800; font-size: 1.1rem; margin-top: 15px; }
    .stButton>button { width: 100%; background-color: #ff6b6b; color: white; border: none; border-radius: 8px; height: 42px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 2. 주차별 상세 가이드 및 성경 구절 데이터
def get_comprehensive_guide(weeks):
    guides = {
        0: {"baby": "새 생명을 맞이할 준비를 하고 있어요.", "mom": "임신 준비기입니다. 몸을 따뜻하게 유지하고 엽산 복용을 시작하세요.", "dad": "함께 금주하고 아내의 컨디션을 세심히 살펴주세요.", "caution": "약물 복용 전 반드시 전문가와 상의하세요."},
        4: {"baby": "양귀비 씨앗 크기! 세포 분열이 활발해요.", "mom": "착상 시기라 무리한 운동은 금물입니다. 충분한 휴식을 취하세요.", "dad": "임신 테스트기 확인 후, 따뜻한 축하와 꽃 한 송이를 선물해 보세요.", "caution": "대중교통 이용 시 가방 고리를 활용해 배려받으세요."},
        8: {"baby": "라즈베리 크기! 심장 소리를 들을 수 있어요.", "mom": "입덧이 가장 심해지는 시기입니다. 차가운 음식이나 신 과일이 도움이 돼요.", "dad": "집안 음식 냄새를 차단해주고, 아내가 먹고 싶어 하는 것을 바로 구해주세요.", "caution": "출혈이나 심한 복통이 있다면 즉시 병원을 방문하세요."},
        12: {"baby": "라임 크기! 이제 제법 사람의 모습을 갖췄어요.", "mom": "기형아 검사 시기입니다. 정서적 안정이 가장 중요해요.", "dad": "초음파 검사에 꼭 동행해서 아기의 첫 움직임을 함께 보세요.", "caution": "기초 체온이 높아 감기로 오해하기 쉬우니 약 복용 주의!"},
        16: {"baby": "아보카도 크기! 뼈가 단단해지고 소리를 들어요.", "mom": "철분제 복용 시작! 변비가 올 수 있으니 수분 섭취를 늘리세요.", "dad": "아내의 배에 귀를 대고 이레에게 아빠 목소리를 들려주세요.", "caution": "갑작스러운 기립성 저혈압(어지럼증)을 조심하세요."},
        20: {"baby": "바나나 길이! 태동이 느껴지기 시작합니다.", "mom": "체중이 급격히 늘 수 있으니 가벼운 산책을 생활화하세요.", "dad": "태동이 느껴질 때 같이 손을 얹어 교감해 주세요.", "caution": "임신 중기지만 무거운 물건을 드는 것은 피해야 합니다."},
        24: {"baby": "옥수수 크기! 빛과 소리에 반응합니다.", "mom": "임신성 당뇨 검사가 있습니다. 단 음식 섭취를 조절하세요.", "dad": "허리 통증이 심해질 시기니 자기 전 다리 마사지를 꼭 해주세요.", "caution": "배 뭉침이 잦다면 즉시 하던 일을 멈추고 쉬어야 합니다."}
    }
    current = max([w for w in guides.keys() if w <= weeks] + [0])
    return guides[current]

bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고 네가 배에서 나오기 전에 너를 성별하였고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("여인이 어찌 그 젖 먹는 자식을 잊겠으며... 나는 너를 잊지 아니할 것이라", "이사야 49:15"),
    ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라 여호와께서 네 오른쪽에서 네 그늘이 되시나니", "시편 121:5"),
    ("너희는 마음에 근심하지 말라 하나님을 믿으니 또 나를 믿으라", "요한복음 14:1"),
    ("범사에 감사하라 이것이 그리스도 예수 안에서 너희를 향하신 하나님의 뜻이니라", "데살로니가전서 5:18"),
    ("아무 것도 염려하지 말고... 너희 구할 것을 감사함으로 하나님께 아뢰라", "빌립보서 4:6"),
    ("네 길을 여호와께 맡기라 그를 의지하면 그가 이루시고", "시편 37:5")
]

# 3. 사이드바 (타이틀 - 성경구절 - 날짜 순서)
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#ff6b6b; margin-bottom:10px;'>💖 이레 엄마 가이드</h3>", unsafe_allow_html=True)
    
    # [추가] 매일 바뀌는 성경 구절 (날짜를 시드로 사용하여 하루 한 번 변경)
    random.seed(datetime.now().strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f"""
        <div class="bible-box">
            "{verse}"
            <span class="bible-ref">- {ref} -</span>
        </div>
    """, unsafe_allow_html=True)

    # 날짜 설정
    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 4, 9).date())
    due_date = lmp_date + timedelta(days=280)
    today = datetime.now().date()
    total_days = max(0, (today - lmp_date).days)
    current_weeks = total_days // 7
    current_days = total_days % 7
    d_day = (due_date - today).days

    st.markdown(f"""
        <div class="sb-box" style="text-align:center;">
            <span style="font-size:0.85rem; color:gray;">이레는 지금</span><br>
            <span style="font-size:1.6rem; font-weight:800; color:#ff4757;">{current_weeks}주 {current_days}일차</span><br>
            <b style="color:#ff6b6b; font-size:1.1rem;">D-{d_day if d_day > 0 else 'Day!'}</b><br>
            <small style="color:#999;">예정일: {due_date.strftime('%Y-%m-%d')}</small>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🌡️ 오늘 엄마 컨디션 기록"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], key="cond_slider", label_visibility="collapsed")
        memo = st.text_input("메모", placeholder="아빠에게 남길 말", key="cond_memo")
        if st.button("구글 시트 전송", key="btn_cond"):
            if save_to_sheets("컨디션", memo, cond): st.toast("기록 완료! ❤️")
            else: st.error("전송 실패")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("이레에게...", placeholder="소중한 기록을 남겨보세요.", key="letter_area")
        if st.button("기록 저장", key="btn_letter"):
            if save_to_sheets("태교편지", letter): st.success("저장 완료! ❤️")
            else: st.error("저장 실패")

    st.divider()
    st.markdown("<div style='text-align:center; font-size:0.8rem; color:gray;'>임산부 약물/음식 상담</div>", unsafe_allow_html=True)
    st.markdown("<div class='ms-footer'>📞 마더세이프<br>1588-7309</div>", unsafe_allow_html=True)

# 4. 메인 화면 (가이드 및 챗봇)
st.markdown("<h2 style='text-align:center; color:#ff6b6b; margin-bottom:25px;'>💖 이레엄마 안심 가이드</h2>", unsafe_allow_html=True)

guide = get_comprehensive_guide(current_weeks)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="status-card">
        <div class="guide-header">👶 {current_weeks}주차 이레의 상태</div>
        <div class="guide-content">
            {guide['baby']}<br><br>
            <b>엄마의 준비:</b> {guide['mom']}
            <div class="caution-text">⚠️ 주의사항: {guide['caution']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="status-card">
        <div class="guide-header">🙋‍♂️ 이레 아빠의 역할</div>
        <div class="guide-content">
            이번 주 아빠의 미션: <b>"{guide['dad']}"</b><br><br>
            이레 엄마, 오늘도 이레를 품어주느라 고생 많았어요. 
            아빠가 항상 옆에서 지켜줄게요. 사랑해요!
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차네. 오늘 기분은 어때? 🥰"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if prompt := st.chat_input("증상을 물어보거나 대화를 나눠보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        sys_msg = {"role": "system", "content": f"산부인과 전문의 이레 아빠야. 현재 {current_weeks}주차인 아내에게 다정하게 답하고 사랑한다고 해줘."}
        res = client.chat.completions.create(model="gpt-4o", messages=[sys_msg] + st.session_state.messages)
        msg = res.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
