import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 (모바일 최적화)
st.set_page_config(
    page_title="태하 안심 가이드", 
    page_icon="💖",
    layout="centered"
)

# 2. 커스텀 디자인 (가독성 강화)
st.markdown("""
    <style>
    .stApp { background-color: #fffafb; }
    h1 { 
        color: #ff6b6b; 
        font-size: 1.8rem !important; 
        line-height: 1.4;
        word-break: keep-all;
    }
    .stChatMessage { border-radius: 15px; font-size: 16px !important; }
    .stChatInputContainer { padding-bottom: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (주차별 전문 정보)
with st.sidebar:
    st.header("❤️ 태하네 행복 가이드")
    st.markdown("태하 엄마를 위해 아빠가 만든 **전문가급 안심 가이드**")
    st.divider()

    st.subheader("📅 주차별 의학 정보")
    week = st.selectbox(
        "현재 주차를 선택하세요",
        [f"{i}주차" for i in range(1, 13)] + ["중기(13~27주)", "후기(28주~ )"]
    )

    # 전문 의학 근거 기반 주차별 팁
    week_info = {
        "1주차": "마지막 생리 시작일입니다. 임신 준비를 위해 엽산 400~800mcg 복용을 시작하세요.",
        "2주차": "배란기입니다. 기초체온 변화에 유의하며 규칙적인 생활을 유지하세요.",
        "3주차": "수정 및 착상 시기입니다. 고열이나 무리한 약물 복용은 피해야 합니다.",
        "4주차": "임신 확인 가능기. 태아의 신경관이 형성되기 시작하므로 금연, 금주는 필수입니다.",
        "5주차": "아기집과 난황 확인 시기. 입덧(오심)이 시작될 수 있으며 수분 섭취가 중요합니다.",
        "6주차": "심장박동 확인 가능. 태아의 주요 장기가 형성되는 '결정적 시기'이므로 약물 사용 전 반드시 상담하세요.",
        "7주차": "뇌포와 사지 싹이 발달합니다. 충분한 수면과 균형 잡힌 영양소 섭취가 필요합니다.",
        "8주차": "태아기 진입. 태아의 움직임이 활발해집니다. 아빠와의 교감이 정서 발달에 도움을 줍니다.",
        "9주차": "안면 구조 형성기. 카페인 섭취를 하루 200mg(커피 1잔) 이하로 제한하세요.",
        "10주차": "태아의 장기가 대부분 형성되었습니다. 치과 치료가 필요한 경우 안정기에 대비해 계획하세요.",
        "11주차": "입덧 절정기. 소량씩 자주 먹는 식이요법이 권장됩니다. 탈수 증상을 모니터링하세요.",
        "12주차": "1차 정밀 초음파 및 NT(목덜미 투명대) 검사 시기입니다. 유산 위험이 급격히 낮아집니다.",
        "중기(13~27주)": "철분제 복용을 시작하고 임신성 당뇨 검사를 준비하세요. 적절한 체중 관리가 필요합니다.",
        "후기(28주~ )": "태동 검사와 백일해 주사 접종을 고려하세요. 분만 징후(진통, 파수)를 숙지해야 합니다."
    }
    
    st.success(f"**[{week} 의학 가이드]**\n\n{week_info[week]}")
    
    st.divider()
    st.subheader("📌 전문 상담 기관")
    st.write("📞 마더세이프: 1588-7309")
    st.caption("※ 본 정보는 보조적인 수단이며, 실제 진단은 전문의의 대면 진료를 우선합니다.")

# 4. 메인 화면
st.title("💖 태하 엄마를 위해 아빠가 만든 안심가이드")

# 5. OpenAI API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    # 시스템 페르소나 강화: 전 세계 최고 권위의 의사이자 다정한 남편
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """너는 전 세계에서 가장 유명하고 신뢰받는 산부인과 전문의이자, 사용자인 '태하 엄마'의 다정한 남편이야.
            너의 답변 원칙은 다음과 같아:
            1. 모든 정보는 추측이 아닌 세계보건기구(WHO), 마더세이프, 산부인과학회 가이드라인 등 '객관적 의학 근거'에 기반해야 한다.
            2. 전문 용어는 사용하되 아내가 이해하기 쉽게 풀어서 설명해주며, 말투는 세상에서 가장 다정하고 따뜻한 남편의 '해요체'를 사용한다.
            3. 약물에 대해서는 마더세이프 데이터를 최우선으로 참고하여 안전 등급을 정확히 안내한다.
            4. 답변 끝에는 반드시 태하와 아내를 향한 사랑의 메시지나 정서적인 응원을 덧붙인다.
            5. 의학적으로 모호한 상황에서는 반드시 '담당 주치의와 상의'할 것을 권고하며 안전을 최우선으로 한다."""
        }
    ]

# 6. 채팅 출력
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. 채팅 입력
if prompt := st.chat_input("태하랑 엄마, 궁금한 게 있나요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
