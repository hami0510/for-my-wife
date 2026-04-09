import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import random

# 1. 페이지 설정
st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="centered")

# 2. 디자인 및 레이아웃 최적화 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Noto Sans KR', sans-serif; background-color: #fffafb; }
    .title-container { padding: 2rem 0rem 1rem 0rem; text-align: center; }
    .main-title { color: #ff6b6b; font-size: 1.8rem !important; font-weight: 700; line-height: 1.4; }
    
    .bible-box { 
        background-color: #fdf2f2; 
        padding: 15px; 
        border-radius: 12px; 
        border-left: 4px solid #ff8787;
        margin-bottom: 20px;
        font-size: 0.85rem;
        color: #444;
        line-height: 1.6;
    }
    .bible-ref { font-weight: bold; color: #ff6b6b; display: block; margin-top: 5px; text-align: right; }

    .cheer-box { background: white; padding: 15px; border-radius: 12px; border: 1px dashed #ffb6c1; text-align: center; margin-bottom: 20px; font-style: italic; color: #ff6b6b; }
    .guide-box { padding: 15px; border-radius: 12px; margin-bottom: 12px; font-size: 0.9rem; line-height: 1.6; }
    .mom-guide { background-color: #f1f8ff; border-left: 4px solid #74c0fc; color: #1971c2; }
    .dad-guide { background-color: #fff9db; border-left: 4px solid #fab005; color: #925400; }
    .call-box { display: block; background-color: #ff6b6b; color: white !important; text-align: center; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 정의
bible_verses = [
    ("내가 너를 모태에 짓기 전에 너를 알았고 네가 배에서 나오기 전에 너를 성별하였고...", "예레미야 1:5"),
    ("자식들은 여호와의 기업이요 태의 열매는 그의 상급이로다", "시편 127:3"),
    ("여인이 어찌 그 젖 먹는 자식을 잊겠으며 자기 태에서 난 아들을 긍휼히 여기지 않겠느냐 그들은 혹시 잊을지라도 나는 너를 잊지 아니할 것이라", "이사야 49:15"),
    ("주께서 내 내장을 지으시며 나의 모태에서 나를 만드셨나이다", "시편 139:13"),
    ("여호와는 너를 지키시는 이시라 여호와께서 네 오른쪽에서 네 그늘이 되시나니", "시편 121:5"),
    ("너희는 마음에 근심하지 말라 하나님을 믿으니 또 나를 믿으라", "요한복음 14:1"),
    ("범사에 감사하라 이것이 그리스도 예수 안에서 너희를 향하신 하나님의 뜻이니라", "데살로니가전서 5:18"),
    ("아무 것도 염려하지 말고 다만 모든 일에 기도와 간구로, 너희 구할 것을 감사함으로 하나님께 아뢰라", "빌립보서 4:6"),
    ("네 길을 여호와께 맡기라 그를 의지하면 그가 이루시고", "시편 37:5")
]

baby_sizes = {
    "1주차": "씨앗", "2주차": "작은 점", "3주차": "좁쌀", "4주차": "양귀비 씨앗",
    "5주차": "사과 씨앗", "6주차": "완두콩", "7주차": "블루베리", "8주차": "라즈베리",
    "9주차": "체리", "10주차": "딸기", "11주차": "무화과", "12주차": "라임",
    "중기(13~27주)": "달콤한 멜론", "후기(28주~ )": "커다란 수박"
}

cheer_messages = [
    "이레 엄마, 오늘 하루도 정말 고생 많았어! ❤️",
    "세상에서 가장 예쁜 임산부, 오늘도 화이팅! ✨",
    "우리 이레랑 엄마, 아빠가 항상 지켜줄게. 사랑해! 🥰",
    "오늘 컨디션은 어때? 힘들면 언제든 아빠한테 말해줘! 🤙",
    "이레가 엄마 닮아서 아주 예쁠 것 같아! 고마워. 🌸"
]

# 4. 사이드바 구성
with st.sidebar:
    st.markdown("### ❤️ 이레네 행복 가이드")
    
    random.seed(datetime.now().strftime("%Y%m%d"))
    verse, ref = random.choice(bible_verses)
    st.markdown(f"""
        <div class="bible-box">
            " {verse} "
            <span class="bible-ref">- {ref} -</span>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("#### 📅 예정일 계산기")
    base_date = st.date_input("마지막 생리 시작일(LMP)", datetime.now())
    due_date = base_date + timedelta(days=280)
    d_day = (due_date - datetime.now().date()).days
    st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #ffe3e3; text-align: center;">
            <div style="color: #ff6b6b; font-size: 0.85rem; font-weight: bold;">이레를 만나는 날까지</div>
            <div style="color: #ff4757; font-size: 1.8rem; font-weight: 800; margin: 8px 0;">D-{d_day if d_day > 0 else 'Day!'}</div>
            <div style="font-size: 0.8rem; color: #999;">예정일: {due_date.strftime('%Y년 %m월 %d일')}</div>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("#### 💡 주차별 가이드")
    week = st.selectbox("주차 선택", list(baby_sizes.keys()), label_visibility="collapsed")
    guides = {
        "1주차": {"mom": "임신 준비기! 엽산 복용을 시작하세요.", "dad": "함께 엽산을 복용하고 금연/금주를 시작하세요."},
        "2주차": {"mom": "배란기입니다. 몸을 따뜻하게 유지하세요.", "dad": "아내가 스트레스 받지 않게 편안한 환경을 만드세요."},
        "3주차": {"mom": "착상 시기예요. 가벼운 산책이 좋아요.", "dad": "아내가 무거운 짐을 들지 않도록 도와주세요."},
        "4주차": {"mom": "임신 확인! 비타민과 영양에 신경 쓰세요.", "dad": "기쁜 소식을 축하하며 꽃 한 송이 선물 어떨까요?"},
        "5주차": {"mom": "입덧 시작 가능성. 조금씩 자주 드세요.", "dad": "음식 냄새에 예민할 수 있으니 환기에 신경 쓰세요."},
        "6주차": {"mom": "심장 소리 확인! 약물 복용은 금물입니다.", "dad": "산부인과 검진에 꼭 동행해서 첫 소리를 같이 들으세요."},
        "7주차": {"mom": "쉽게 피로해집니다. 낮잠을 충분히 자세요.", "dad": "설거지, 청소 등 집안일을 전담해서 아내를 쉬게 하세요."},
        "8주차": {"mom": "정서적 변화가 커요. 기분 전환이 필요해요.", "dad": "아내의 고민을 묵묵히 들어주고 공감해 주세요."},
        "9주차": {"mom": "카페인을 줄이고 과일/채소를 섭취하세요.", "dad": "아내가 먹고 싶어 하는 음식을 적극 챙겨주세요."},
        "10주차": {"mom": "치아 건강 주의! 양치를 꼼꼼히 하세요.", "dad": "태아의 성장을 공부하며 태명을 자주 불러주세요."},
        "11주차": {"mom": "입덧 절정기. 무리하지 말고 안정을 취하세요.", "dad": "손발 마사지를 해주며 혈액순환을 도와주세요."},
        "12주차": {"mom": "1차 검사 통과! 이제 안정기 진입 단계입니다.", "dad": "그동안 고생한 아내에게 고맙다는 편지를 써보세요."},
        "중기(13~27주)": {"mom": "태동이 느껴져요! 철분제를 꼭 챙기세요.", "dad": "배에 귀를 대고 이레에게 동화책을 읽어주세요."},
        "후기(28주~ )": {"mom": "출산 가방을 준비하고 호흡법을 연습하세요.", "dad": "언제든 병원에 갈 수 있게 차량 점검을 하세요."}
    }

    st.markdown(f"""
        <div style="text-align: center; margin: 10px 0; font-size: 0.9rem;">
            지금 우리 이레는 <b>{baby_sizes[week]}</b>만큼 컸어요! 🐥
        </div>
        <div class="guide-box mom-guide"><b>👩‍⚕️ 의학 가이드</b><br>{guides[week]['mom']}</div>
        <div class="guide-box dad-guide"><b>🙋‍♂️ 아빠 가이드</b><br>{guides[week]['dad']}</div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="tel:1588-7309" class="call-box">📞 마더세이프: 1588-7309</a>', unsafe_allow_html=True)

# 5. 메인 화면
st.markdown(f"""
    <div class="title-container">
        <div class="main-title">💖 이레 엄마를 위해<br>아빠가 만든 안심가이드</div>
        <div class="sub-title">의학적 근거와 아빠의 사랑이 담긴 실시간 챗봇</div>
    </div>
    <div class="cheer-box">{random.choice(cheer_messages)}</div>
    """, unsafe_allow_html=True)

# 6. OpenAI 챗봇 로직
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
