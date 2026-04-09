import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import random

# 1. 페이지 설정
st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="centered")

# 2. 고도로 최적화된 CSS (여백 및 가독성 중심)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Noto Sans KR', sans-serif; background-color: #fffafb; }
    
    /* 사이드바 전체 여백 줄이기 */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.5rem !important; padding-top: 1rem !important; }
    
    /* 성경 구절 박스 슬림화 */
    .bible-box { 
        background-color: #fdf2f2; padding: 10px 12px; border-radius: 8px; border-left: 3px solid #ff8787;
        margin-bottom: 5px; font-size: 0.8rem; color: #444; line-height: 1.4;
    }
    .bible-ref { font-weight: bold; color: #ff6b6b; display: block; margin-top: 3px; text-align: right; font-size: 0.75rem; }

    /* D-Day 카드 슬림화 */
    .dday-card {
        background: white; padding: 10px; border-radius: 10px; border: 1px solid #ffe3e3; 
        text-align: center; margin-bottom: 5px;
    }
    .dday-title { color: #ff6b6b; font-size: 0.75rem; font-weight: bold; }
    .dday-value { color: #ff4757; font-size: 1.4rem; font-weight: 800; margin: 2px 0; }
    .dday-date { font-size: 0.7rem; color: #999; }

    /* 가이드 박스 슬림화 */
    .guide-box { padding: 10px; border-radius: 8px; margin-bottom: 6px; font-size: 0.82rem; line-height: 1.4; }
    .mom-guide { background-color: #f1f8ff; border-left: 3px solid #74c0fc; color: #1971c2; }
    .dad-guide { background-color: #fff9db; border-left: 3px solid #fab005; color: #925400; }
    
    /* 전화 버튼 슬림화 */
    .call-box { 
        display: block; background-color: #ff6b6b; color: white !important; text-align: center; 
        padding: 8px; border-radius: 8px; text-decoration: none; font-weight: bold; 
        margin-top: 5px; font-size: 0.85rem;
    }

    /* 메인 타이틀 */
    .main-title { color: #ff6b6b; font-size: 1.6rem !important; font-weight: 700; text-align: center; }
    .cheer-box { background: white; padding: 10px; border-radius: 10px; border: 1px dashed #ffb6c1; text-align: center; font-size: 0.85rem; color: #ff6b6b; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 및 로직
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라 여호와께서 네 그늘이 되시나니", "시편 121:5"),
    ("네 길을 여호와께 맡기라 그를 의지하면 그가 이루시고", "시편 37:5")
]

baby_sizes = {"1주차": "씨앗", "2주차": "작은 점", "3주차": "좁쌀", "4주차": "양귀비 씨앗", "5주차": "사과 씨앗", "6주차": "완두콩", "7주차": "블루베리", "8주차": "라즈베리", "9주차": "체리", "10주차": "딸기", "11주차": "무화과", "12주차": "라임", "중기(13~27주)": "멜론", "후기(28주~ )": "수박"}
cheer_messages = ["이레 엄마, 오늘 하루도 고생 많았어! ❤️", "우리 이레랑 엄마, 아빠가 지켜줄게. 🥰", "이레가 엄마 닮아 예쁠 거야! 고마워. 🌸"]

# 4. 사이드바 (슬림 레이아웃 적용)
with st.sidebar:
    st.markdown("### ❤️ 이레네 가이드")
    
    # 성경 구절
    random.seed(datetime.now().strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f'<div class="bible-box">"{verse}"<span class="bible-ref">- {ref} -</span></div>', unsafe_allow_html=True)

    # D-Day
    base_date = st.date_input("마지막 생리 시작일(LMP)", datetime.now())
    due_date = base_date + timedelta(days=280)
    d_day = (due_date - datetime.now().date()).days
    st.markdown(f"""<div class="dday-card"><div class="dday-title">이레 만나는 날</div><div class="dday-value">D-{d_day if d_day > 0 else 'Day!'}</div><div class="dday-date">예정일: {due_date.strftime('%Y-%m-%d')}</div></div>""", unsafe_allow_html=True)

    # 가이드 섹션
    week = st.selectbox("주차 선택", list(baby_sizes.keys()), label_visibility="collapsed")
    guides = {
        "1주차": {"mom": "임신 준비기! 엽산 복용 시작하세요.", "dad": "함께 금연/금주를 시작하세요."},
        "2주차": {"mom": "배란기입니다. 몸을 따뜻하게 하세요.", "dad": "편안한 환경을 만들어주세요."},
        "3주차": {"mom": "착상 시기예요. 가벼운 산책이 좋아요.", "dad": "무거운 짐은 아빠가 드세요."},
        "4주차": {"mom": "임신 확인! 비타민 챙기세요.", "dad": "꽃 한 송이 선물 어떨까요?"},
        "5주차": {"mom": "입덧 시작 가능성. 조금씩 자주 드세요.", "dad": "음식 냄새 환기에 신경 쓰세요."},
        "6주차": {"mom": "심장 소리 확인! 약물 주의하세요.", "dad": "검진에 꼭 동행해 주세요."},
        "7주차": {"mom": "쉽게 피로합니다. 충분히 자세요.", "dad": "집안일을 전담해 주세요."},
        "8주차": {"mom": "정서적 변화가 커요. 공감해 주세요.", "dad": "이야기를 묵묵히 들어주세요."},
        "9주차": {"mom": "과일/채소를 많이 섭취하세요.", "dad": "먹고 싶은 음식을 챙겨주세요."},
        "10주차": {"mom": "치아 건강 주의! 양치 꼼꼼히 하세요.", "dad": "태명을 자주 불러주세요."},
        "11주차": {"mom": "입덧 절정기. 안정을 취하세요.", "dad": "손발 마사지를 해주세요."},
        "12주차": {"mom": "1차 검사 통과! 안정기 진입입니다.", "dad": "고맙다는 편지를 써보세요."},
        "중기(13~27주)": {"mom": "태동이 느껴져요! 철분제 필수.", "dad": "배에 대고 동화책 읽어주세요."},
        "후기(28주~ )": {"mom": "출산 가방 준비, 호흡 연습하세요.", "dad": "병원 경로를 미리 확인하세요."}
    }
    
    st.markdown(f'<div style="text-align:center; font-size:0.8rem; margin:5px 0;">이레는 <b>{baby_sizes[week]}</b>만 해요! 🐥</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="guide-box mom-guide"><b>👩‍⚕️ 의학:</b> {guides[week]["mom"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="guide-box dad-guide"><b>🙋‍♂️ 아빠:</b> {guides[week]["dad"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<a href="tel:1588-7309" class="call-box">📞 마더세이프 상담</a>', unsafe_allow_html=True)

# 5. 메인 화면
st.markdown(f'<div class="title-container"><div class="main-title">💖 이레 엄마를 위해<br>아빠가 만든 안심가이드</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="cheer-box">{random.choice(cheer_messages)}</div>', unsafe_allow_html=True)

# 6. OpenAI 챗봇
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "너는 세계 최고 산부인과 의사이자 이레 아빠야. 다정한 해요체로 의학 근거에 기반해 답변해줘."}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("이레랑 엄마, 궁금한 게 있나요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
