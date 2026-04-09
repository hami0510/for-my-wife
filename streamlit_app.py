import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import random

# 1. 페이지 설정
st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="centered")

# 2. 화사하고 깔끔한 디자인 최적화 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #fffafb; 
    }
    
    /* 사이드바 요소 간격 조절 */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 1rem !important; }
    
    /* 성경 구절 박스 (이전의 감성적인 디자인) */
    .bible-box { 
        background-color: #fdf2f2; padding: 15px; border-radius: 12px; border-left: 4px solid #ff8787;
        margin-bottom: 10px; font-size: 0.9rem; color: #444; line-height: 1.6;
    }
    .bible-ref { font-weight: bold; color: #ff6b6b; display: block; margin-top: 5px; text-align: right; }

    /* D-Day 카드 (이전의 시원한 디자인) */
    .dday-card {
        background: white; padding: 15px; border-radius: 12px; border: 1px solid #ffe3e3; 
        text-align: center; margin-bottom: 10px;
    }
    .dday-title { color: #ff6b6b; font-size: 0.85rem; font-weight: bold; }
    .dday-value { color: #ff4757; font-size: 1.6rem; font-weight: 800; margin: 8px 0; }
    .dday-date { font-size: 0.8rem; color: #999; }

    /* 가이드 박스 (깔끔한 구분) */
    .guide-box { padding: 12px; border-radius: 10px; margin-bottom: 10px; font-size: 0.9rem; line-height: 1.5; }
    .mom-guide { background-color: #f1f8ff; border-left: 5px solid #74c0fc; color: #1971c2; }
    .dad-guide { background-color: #fff9db; border-left: 5px solid #fab005; color: #925400; }
    
    /* 마더세이프 전화 버튼 */
    .call-box { 
        display: block; background-color: #ff6b6b; color: white !important; text-align: center; 
        padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; 
        font-size: 0.95rem; margin-top: 5px;
    }

    /* 메인 화면 타이틀 및 응원 박스 */
    .main-title { color: #ff6b6b; font-size: 1.8rem !important; font-weight: 700; text-align: center; line-height: 1.4; }
    .cheer-box { 
        background: white; padding: 15px; border-radius: 12px; border: 1px dashed #ffb6c1; 
        text-align: center; margin-bottom: 20px; font-style: italic; color: #ff6b6b; font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 정의
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고 네가 배에서 나오기 전에 너를 성별하였고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라 여호와께서 네 오른쪽에서 네 그늘이 되시나니", "시편 121:5"),
    ("네 길을 여호와께 맡기라 그를 의지하면 그가 이루시고", "시편 37:5")
]

baby_sizes = {"1주차": "씨앗", "2주차": "작은 점", "3주차": "좁쌀", "4주차": "양귀비 씨앗", "5주차": "사과 씨앗", "6주차": "완두콩", "7주차": "블루베리", "8주차": "라즈베리", "9주차": "체리", "10주차": "딸기", "11주차": "무화과", "12주차": "라임", "중기(13~27주)": "달콤한 멜론", "후기(28주~ )": "커다란 수박"}
cheer_messages = ["이레 엄마, 오늘 하루도 정말 고생 많았어! ❤️", "우리 이레랑 엄마, 아빠가 항상 지켜줄게. 🥰", "이레가 엄마 닮아서 아주 예쁠 것 같아! 고마워. 🌸", "오늘 컨디션은 어때? 힘들면 언제든 아빠한테 말해줘! ✨"]

# 4. 사이드바 구성
with st.sidebar:
    st.markdown("### ❤️ 이레네 행복 가이드")
    
    # 성경 구절
    random.seed(datetime.now().strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f'<div class="bible-box">"{verse}"<span class="bible-ref">- {ref} -</span></div>', unsafe_allow_html=True)

    st.divider()

    # D-Day 및 예정일
    st.markdown("#### 📅 예정일 계산기")
    base_date = st.date_input("마지막 생리 시작일(LMP)", datetime.now())
    due_date = base_date + timedelta(days=280)
    d_day = (due_date - datetime.now().date()).days
    st.markdown(f"""
        <div class="dday-card">
            <div class="dday-title">이레를 만나는 날까지</div>
            <div class="dday-value">D-{d_day if d_day > 0 else 'Day!'}</div>
            <div class="dday-date">예정일: {due_date.strftime('%Y년 %m월 %d일')}</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 주차별 가이드 섹션
    st.markdown("#### 💡 주차별 가이드")
    week = st.selectbox("주차 선택", list(baby_sizes.keys()), label_visibility="collapsed")
    guides = {
        "1주차": {"mom": "임신 준비기! 엽산 복용을 시작하세요.", "dad": "함께 엽산을 복용하고 금연/금주를 시작하세요."},
        "2주차": {"mom": "배란기입니다. 몸을 따뜻하게 유지하세요.", "dad": "아내가 스트레스 받지 않게 편안한 환경을 만드세요."},
        "3주차": {"mom": "착상 시기예요. 가벼운 산책이 좋아요.", "dad": "아내가 무거운 짐을 들지 않도록 도와주세요."},
        "4주차": {"mom": "임신 확인! 비타민과 영양에 신경 쓰세요.", "dad": "기쁜 소식을 축하하며 꽃 한 송이 선물 어떨까요?"},
        "5주차": {"mom": "입덧 시작 가능성. 조금씩 자주 드세요.", "dad": "음식 냄새 환기에 신경 쓰세요."},
        "6주차": {"mom": "심장 소리 확인! 약물 복용은 금물입니다.", "dad": "산부인과 검진에 꼭 동행해서 첫 소리를 같이 들으세요."},
        "7주차": {"mom": "쉽게 피로해집니다. 낮잠을 충분히 자세요.", "dad": "집안일을 전담해서 아내를 쉬게 하세요."},
        "8주차": {"mom": "정서적 변화가 커요. 기분 전환이 필요해요.", "dad": "아내의 고민을 묵묵히 들어주고 공감해 주세요."},
        "9주차": {"mom": "카페인을 줄이고 과일/채소를 섭취하세요.", "dad": "아내가 먹고 싶어 하는 음식을 적극 챙겨주세요."},
        "10주차": {"mom": "치아 건강 주의! 양치를 꼼꼼히 하세요.", "dad": "태아의 성장을 공부하며 태명을 자주 불러주세요."},
        "11주차": {"mom": "입덧 절정기. 무리하지 말고 안정을 취하세요.", "dad": "손발 마사지를 해주며 혈액순환을 도와주세요."},
        "12주차": {"mom": "1차 검사 통과! 이제 안정기 진입 단계입니다.", "dad": "그동안 고생한 아내에게 고맙다는 편지를 써보세요."},
        "중기(13~27주)": {"mom": "태동이 느껴져요! 철분제를 꼭 챙기세요.", "dad": "배에 귀를 대고 이레에게 동화책을 읽어주세요."},
        "후기(28주~ )": {"mom": "출산 가방을 준비하고 호흡법을 연습하세요.", "dad": "언제든 병원에 갈 수 있게 차량 점검을 하세요."}
    }
    
    st.markdown(f'<div style="text-align: center; margin-bottom: 10px; font-size: 0.9rem;">지금 우리 이레는 <b>{baby_sizes[week]}</b>만 해요! 🐥</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="guide-box mom-guide"><b>👩‍⚕️ 의학 가이드</b><br>{guides[week]["mom"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="guide-box dad-guide"><b>🙋‍♂️ 아빠 가이드</b><br>{guides[week]["dad"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<a href="tel:1588-7309" class="call-box">📞 마더세이프 상담: 1588-7309</a>', unsafe_allow_html=True)

# 5. 메인 화면
st.markdown(f"""
    <div class="title-container">
        <div class="main-title">💖 이레 엄마를 위해<br>아빠가 만든 안심가이드</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown(f'<div class="cheer-box">{random.choice(cheer_messages)}</div>', unsafe_allow_html=True)

# 6. OpenAI 챗봇
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "너는 세계 최고 산부인과 의사이자 이레 아빠야. 다정한 해요체로 의학 근거에 기반해 답변해줘."}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("이레랑 엄마, 무엇이 궁금한가요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
