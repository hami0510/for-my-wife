import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta, timezone
import requests
import json
import re
import base64

# ==========================================
# 핵심 설정
# ==========================================
REAL_SHEET_URL = "https://docs.google.com/spreadsheets/d/1r2LdeqpfhhH5IAmt_ef4Z6RuQ4M5-_V6_tNz-2dpY-E/edit?gid=0#gid=0"
GAS_URL = "https://script.google.com/macros/s/AKfycbyD3Cs7lzrU-npU976mBQirH1AmHrWRHggDjF8l5mYPFllREHaZ1WUqyZag4viWsmdIJQ/exec"

st.set_page_config(page_title="이레 안심 가이드", page_icon="💖", layout="wide")

def save_to_sheets(type_val, content, status=""):
    data = {"type": type_val, "content": content, "status": status}
    try:
        r = requests.post(GAS_URL, data=json.dumps(data), headers={"Content-Type": "application/json"}, timeout=10)
        return r.status_code == 200
    except Exception:
        return False

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #fdf6f8 !important;
    color: #333 !important;
}
[data-testid="stHeader"] { height: 0 !important; min-height: 0 !important; }
[data-testid="stAppViewBlockContainer"] { padding-top: 1rem !important; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; }
[data-testid="collapsedControl"] {
    display: block !important; visibility: visible !important;
    background-color: #ff6b6b !important; border-radius: 0 12px 12px 0 !important;
    padding: 8px 10px !important; box-shadow: 2px 2px 8px rgba(255,107,107,0.4) !important;
}
[data-testid="collapsedControl"] svg { fill: #fff !important; }
[data-testid="stSidebar"] {
    background-color: #fff !important;
    border-right: 1px solid #ffe0e6 !important;
}
h1, h2, h3 { font-family: 'Noto Sans KR', sans-serif !important; }

/* 카드 공통 */
.card {
    background: #fff;
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 4px 18px rgba(255,107,107,0.08);
    border-top: 5px solid #ff6b6b;
}
.card-blue  { border-top-color: #5b8dee; }
.card-green { border-top-color: #2ecc71; }
.card-purple{ border-top-color: #a29bfe; }
.card-orange{ border-top-color: #fd9644; }
.card-teal  { border-top-color: #00cec9; }
.card-red   { border-top-color: #e74c3c; }

.card-title {
    font-size: 1.1rem; font-weight: 800;
    color: #ff6b6b; margin-bottom: 10px;
}
.card-title-blue   { color: #5b8dee; }
.card-title-green  { color: #27ae60; }
.card-title-purple { color: #6c5ce7; }
.card-title-orange { color: #e67e22; }
.card-title-teal   { color: #00b894; }
.card-title-red    { color: #e74c3c; }

.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 0.78rem; font-weight: 700;
    margin: 3px 3px 3px 0;
}
.badge-red    { background: #ffe0e0; color: #e74c3c; }
.badge-blue   { background: #ddeeff; color: #2c7be5; }
.badge-green  { background: #d5f5e3; color: #27ae60; }
.badge-purple { background: #ede7f6; color: #6c3483; }
.badge-orange { background: #fef9e7; color: #e67e22; }
.badge-gray   { background: #f0f0f0; color: #666; }

.week-hero {
    background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
    color: #fff; border-radius: 22px; padding: 28px 30px;
    margin-bottom: 22px; text-align: center;
}
.week-hero h1 { color: #fff !important; font-size: 2.2rem; margin: 0; }
.week-hero p  { color: rgba(255,255,255,0.9); margin: 6px 0 0; font-size: 1rem; }

.food-ok   { color: #27ae60; font-weight: 700; }
.food-no   { color: #e74c3c; font-weight: 700; }
.food-warn { color: #e67e22; font-weight: 700; }

.flow-step {
    background:#fff; border-radius:12px; padding:12px 16px; margin-bottom:8px;
    border-left:4px solid #e74c3c; box-shadow:0 2px 8px rgba(0,0,0,0.04);
    font-size:0.92rem; line-height:1.6;
}
.flow-num {
    display:inline-block; background:#e74c3c; color:#fff; font-weight:800;
    width:24px; height:24px; border-radius:50%; text-align:center; line-height:24px;
    margin-right:8px; font-size:0.85rem;
}

.milestone-box {
    background:#fff8f0; border-radius:12px; padding:10px 14px; margin-bottom:8px;
    border-left:4px solid #fd9644; font-size:0.85rem;
}

.sidebar-title { font-size:1.3rem; font-weight:800; color:#ff6b6b; text-align:center; display:block; padding-top:8px; }
.sidebar-today { font-size:0.85rem; color:#888; text-align:center; margin-bottom:12px; display:block; }
.bible-box {
    background:#fff0f3; padding:16px; border-radius:14px;
    border-left:5px solid #ff6b6b; margin-bottom:16px;
    font-size:0.88rem; line-height:1.7; color:#555;
}
.bible-ref { display:block; text-align:right; font-weight:700; color:#ff6b6b; margin-top:8px; font-size:0.82rem; }
.sb-box {
    background:#fff; border:1px solid #ffe3e3; border-radius:14px;
    padding:16px; text-align:center; margin-bottom:14px;
}
.stButton>button {
    width:100%; background-color:#ff6b6b !important; color:#fff !important;
    border-radius:10px; height:44px; font-weight:700;
}
div[data-testid="stChatInput"] {
    background:#fff !important; border-radius:22px !important;
    padding:5px 15px !important; border:2px solid #ffe3e3 !important;
}
.stTabs [data-baseweb="tab"] { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 성경 구절 31일 순환
# ==========================================
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
    ("너는 마음에 새기고 네 자녀에게 부지런히 가르치며...", "신명기 6:6"),
]

# ==========================================
# 전체 40주 상세 데이터
# ==========================================
WEEK_DATA = {
    1:  {"size": "씨앗 (1mm)", "fetal": "수정란이 자궁으로 이동 중이에요. 세포 분열이 시작됩니다.", "mom": "아직 임신 증상이 없을 수 있어요. 엽산 400~800㎍을 꼭 복용하세요.", "dad": "함께 금주·금연을 시작하고 엽산 복용을 챙겨주세요.", "caution": "방사선(엑스레이) 노출 주의, 약물 복용 전 전문가 상담 필수"},
    2:  {"size": "참깨 (1~2mm)", "fetal": "착상이 진행됩니다. hCG 호르몬이 분비되기 시작해요.", "mom": "착상혈(소량의 갈색 출혈)이 있을 수 있어요. 자연스러운 현상입니다.", "dad": "안정된 환경을 만들어 주세요. 과격한 운동이나 무거운 짐 드는 것을 삼가 주세요.", "caution": "심한 복통이나 선홍색 출혈 시 즉시 병원 방문"},
    3:  {"size": "쌀알 (2mm)", "fetal": "신경관, 척추, 뇌의 기초가 형성되기 시작해요.", "mom": "가슴이 예민해지고 소변이 잦아질 수 있어요.", "dad": "입덧 대비 소화가 잘 되는 음식을 준비해 두세요.", "caution": "엽산 복용이 신경관 결손 예방에 매우 중요해요"},
    4:  {"size": "양귀비씨 (2~3mm)", "fetal": "심장이 뛰기 시작! 머리·몸통·팔다리의 기초가 생겨요.", "mom": "입덧이 슬슬 시작될 수 있어요. 피로감이 심해집니다.", "dad": "집안일을 적극 도와주고, 향이 강한 음식 조리를 대신 해주세요.", "caution": "과도한 카페인(하루 200mg 이하), 날 음식 주의"},
    5:  {"size": "참깨 묶음 (4~5mm)", "fetal": "심장박동이 분당 100회! 손·발 형태가 나타나요.", "mom": "입덧이 본격화됩니다. 오전에 특히 심할 수 있어요.", "dad": "냄새에 민감하니 환기를 자주 해주고, 좋아하는 간식을 찾아보세요.", "caution": "구토가 심해 수분 섭취도 어려우면 병원 방문"},
    6:  {"size": "블루베리 (8~10mm)", "fetal": "눈·코·귀·입이 형성되기 시작해요. 손가락 발가락이 생겨요.", "mom": "유방이 커지고 허리 통증이 올 수 있어요.", "dad": "등 마사지로 허리 통증을 덜어주세요.", "caution": "격렬한 운동 삼가, 사우나·찜질방 고온 노출 주의"},
    7:  {"size": "라즈베리 (13mm)", "fetal": "팔·다리가 움직이기 시작해요. 뇌가 빠르게 발달 중입니다.", "mom": "졸음이 극심해질 수 있어요. 낮잠이 도움이 돼요.", "dad": "충분한 휴식을 취할 수 있도록 환경을 만들어 주세요.", "caution": "생선회, 덜 익힌 고기, 날달걀 섭취 금지"},
    8:  {"size": "딸기 (16mm)", "fetal": "모든 주요 장기의 기초가 완성됩니다. 초음파로 심장소리를 들을 수 있어요!", "mom": "변비가 생길 수 있어요. 섬유질과 수분 섭취를 늘리세요.", "dad": "첫 초음파 검진에 꼭 함께 가세요!", "caution": "유산 위험이 가장 높은 시기—안정이 최우선"},
    9:  {"size": "포도 (23mm)", "fetal": "이제 '태아(fetus)'라고 부릅니다! 눈꺼풀이 생겨요.", "mom": "입덧이 정점에 달할 수 있어요. 차갑고 담백한 음식이 도움돼요.", "dad": "병원 동행, 집안일 전담, 정서적 지지가 가장 큰 선물이에요.", "caution": "고열 시 즉시 병원 방문—태아에게 위험할 수 있어요"},
    10: {"size": "쿠키 (31mm)", "fetal": "손톱이 생기기 시작해요. 뼈가 굳기 시작합니다.", "mom": "허리가 자꾸 아프다면 임산부 벨트를 활용해 보세요.", "dad": "임산부 전용 베개나 쿠션을 선물해 보세요.", "caution": "기형아 검사(NT 초음파) 일정을 확인하세요"},
    11: {"size": "라임 (41mm)", "fetal": "생식기가 형성됩니다. 손발을 쥐었다 펴는 연습을 해요.", "mom": "입덧이 조금씩 나아지기 시작할 수 있어요.", "dad": "이레 이름을 자주 불러주며 태담을 시작해 보세요.", "caution": "1차 기형아 검사(통합선별검사) 11~13주에 받아야 해요"},
    12: {"size": "작은 사과 (55mm)", "fetal": "사람의 모습이 완성됐어요! 눈·코·입이 뚜렷해요.", "mom": "입덧이 줄면서 식욕이 돌아올 수 있어요.", "dad": "임신 소식을 함께 나눌 준비를 해보세요.", "caution": "1차 기형아 검사 마감—놓치지 마세요!"},
    13: {"size": "복숭아 (74mm)", "fetal": "장이 복강 내로 들어왔어요. 성별이 구분되기 시작해요.", "mom": "안정기에 접어듭니다! 유산 위험이 현저히 줄어들어요.", "dad": "태교 여행을 계획해 볼 좋은 시기예요.", "caution": "임신성 고혈압 예방을 위해 짠 음식을 줄이세요"},
    14: {"size": "레몬 (85mm)", "fetal": "얼굴 표정을 짓고, 엄지손가락을 빨기도 해요.", "mom": "배가 눈에 띄게 나오기 시작해요. 임산부 옷을 준비하세요.", "dad": "가슴 부위가 변하는 아내를 따뜻하게 안아주세요.", "caution": "저강도 유산소 운동(걷기, 수영)을 시작하기 좋아요"},
    15: {"size": "배 (100mm)", "fetal": "양수를 마시고 배출하는 연습을 해요. 청각이 발달해요!", "mom": "태동(첫 움직임)을 느낄 수 있어요—'퍼르르' 같은 느낌이에요.", "dad": "배에 귀를 대고 태담을 해주세요. 이레가 들어요!", "caution": "2차 기형아 검사(쿼드 검사) 15~20주 사이에 받으세요"},
    16: {"size": "아보카도 (116mm)", "fetal": "눈이 빛에 반응하고, 다양한 표정을 지을 수 있어요.", "mom": "등, 허리 통증이 심해질 수 있어요. 바른 자세가 중요해요.", "dad": "같이 임산부 체조 영상을 보고 따라 해보세요.", "caution": "치과 치료가 필요하면 이 시기에 받는 것이 좋아요"},
    17: {"size": "무 (130mm)", "fetal": "지방이 쌓이기 시작해요. 골격이 굳어가고 있어요.", "mom": "체중이 빠르게 늘어날 수 있어요. 균형 잡힌 식단이 중요해요.", "dad": "건강한 간식(과일, 견과류)을 챙겨주세요.", "caution": "체중 증가 기준: 전체 임신 기간 11~16kg 이내"},
    18: {"size": "고구마 (143mm)", "fetal": "청력이 완전히 발달해 외부 소리에 반응해요.", "mom": "태동이 뚜렷하게 느껴질 거예요!", "dad": "클래식 음악, 동화책 읽어주기로 태교를 시작해 보세요.", "caution": "정기 초음파로 태아 위치·성장 확인을 받으세요"},
    19: {"size": "망고 (152mm)", "fetal": "뇌 신경세포 연결이 활발해져요. 피부 보호막(태지)이 생겨요.", "mom": "배꼽이 튀어나오기 시작할 수 있어요.", "dad": "함께 아기 침대나 육아용품을 쇼핑해 보세요.", "caution": "대형 기형아 정밀 초음파(20주 전후) 예약을 잡으세요"},
    20: {"size": "바나나 (165mm)", "fetal": "임신 절반! 손가락 지문이 완성됩니다.", "mom": "임신 중기의 황금기—컨디션이 비교적 좋아요.", "dad": "임신 기념 사진 촬영이나 여행을 계획해 보세요.", "caution": "정밀 초음파(대형 기형아 검사) 꼭 받으세요"},
    21: {"size": "당근 (267mm)", "fetal": "눈썹·속눈썹이 생겼어요. 맛을 느낄 수 있어요.", "mom": "발목·발이 붓기 시작할 수 있어요. 다리 올려 쉬세요.", "dad": "발 마사지로 부기를 줄여주세요.", "caution": "쥐가 자주 나면 칼슘·마그네슘 보충을 고려하세요"},
    22: {"size": "옥수수 (280mm)", "fetal": "이제 소리에 놀라는 반응을 해요. 수면·각성 패턴이 생겨요.", "mom": "배가 많이 나와 균형감이 달라질 수 있어요.", "dad": "바닥 물건을 미리 정리해 안전한 환경을 만들어 주세요.", "caution": "임신선 예방을 위해 보습 크림을 꼼꼼히 발라요"},
    23: {"size": "큰 망고 (290mm)", "fetal": "폐 발달이 활발해요. 아직 세상에 나오면 생존이 어려워요.", "mom": "속쓰림이 심해질 수 있어요. 소량씩 자주 드세요.", "dad": "제산제 등 위장약은 임산부 전용인지 확인해 주세요.", "caution": "조산 증상(규칙적 배뭉침, 출혈, 이상 분비물) 즉시 병원 방문"},
    24: {"size": "귀여운 옥수수 (300mm)", "fetal": "뇌가 급격히 발달해요. 눈이 조금씩 뜨이기 시작해요.", "mom": "임신성 당뇨 검사 시기입니다. 꼭 받으세요!", "dad": "단 음식·탄산음료 줄이기를 함께 실천해 주세요.", "caution": "24~28주 사이 임신성 당뇨 선별검사 필수"},
    25: {"size": "순무 (350mm)", "fetal": "손을 활짝 펴고 쥐는 연습을 해요. 반응이 활발해져요.", "mom": "치질이 생길 수 있어요. 섬유질·수분 섭취로 예방하세요.", "dad": "이레 방 꾸미기, 태교 독서를 함께 즐겨요.", "caution": "오른쪽으로 눕는 것보다 왼쪽으로 눕는 것이 혈액순환에 좋아요"},
    26: {"size": "스카치페퍼 (360mm)", "fetal": "눈꺼풀을 뜨고 감을 수 있어요. 눈이 완성돼 가요.", "mom": "골반 통증이 심해질 수 있어요.", "dad": "물건 들기, 무거운 장보기를 대신해 주세요.", "caution": "임신 후기 여행은 주치의와 상담 후 결정하세요"},
    27: {"size": "상추 뭉치 (370mm)", "fetal": "뇌파 활동이 성인과 비슷해져요. 꿈을 꿀 수도 있어요!", "mom": "수면이 어려워질 수 있어요. 임산부 전용 베개를 활용하세요.", "dad": "취침 전 허리·다리 마사지로 편안하게 해주세요.", "caution": "임신 후기(3분기) 시작—정기 검진 2주에 한 번으로"},
    28: {"size": "코코넛 (375mm)", "fetal": "눈이 완전히 열려요. 빛을 감지해요.", "mom": "무거워진 배로 인해 자세가 힘들 수 있어요.", "dad": "태동 차트를 함께 기록해 보세요. 하루 10회 이상이 정상이에요.", "caution": "태동이 갑자기 줄면 즉시 병원 방문"},
    29: {"size": "버터넛 스쿼시 (385mm)", "fetal": "뼈가 완전히 굳어가고, 지방층이 두꺼워져요.", "mom": "소화불량·역류가 심해질 수 있어요. 식후 바로 눕지 마세요.", "dad": "출산 준비 클래스에 함께 등록해 보세요.", "caution": "GBS(B군 연쇄구균) 검사를 35~37주에 받아야 해요"},
    30: {"size": "대형 배추 (400mm)", "fetal": "뇌·신경계가 빠르게 성숙해요. 이제 거꾸로 앉는 연습을 해요.", "mom": "배가 많이 당기고 브랙스턴-힉스(가진통)이 느껴질 수 있어요.", "dad": "병원까지의 루트를 미리 확인하고 주차 위치를 파악해 두세요.", "caution": "가진통 vs 진진통—규칙적이고 점점 강해지면 진진통"},
    31: {"size": "아스파라거스 다발 (415mm)", "fetal": "폐 기능이 거의 완성돼요. 눈이 빛에 집중해요.", "mom": "빈뇨가 심해집니다. 수분은 충분히, 저녁엔 조금 줄여요.", "dad": "병원 가방 목록을 함께 만들어 준비해 두세요.", "caution": "숨이 갑자기 심하게 차거나 가슴이 아프면 즉시 내원"},
    32: {"size": "스쿼시 (430mm)", "fetal": "손톱·발톱이 완성됩니다. 손가락이 매우 뚜렷해요.", "mom": "임신선(튼살)이 빨갛게 생길 수 있어요. 보습이 최선이에요.", "dad": "출산 가방을 미리 꾸려 두세요. 35주 전에는 완성!", "caution": "조기 진통 증상—10분마다 규칙적인 배뭉침 즉시 병원"},
    33: {"size": "파인애플 (440mm)", "fetal": "면역 항체가 엄마에게서 전달돼요. 꽤 통통해졌어요.", "mom": "갈비뼈 아래가 아플 수 있어요—이레가 발로 차는 거예요!", "dad": "분만 호흡법을 함께 연습해 보세요.", "caution": "산전 진찰은 2주 간격, 36주 이후엔 1주 간격으로"},
    34: {"size": "칸탈루프 멜론 (450mm)", "fetal": "폐 계면활성제가 충분해져 조산해도 생존 가능성이 높아요.", "mom": "골반 압박감이 심해져요. 골반 저근 운동(케겔)이 도움돼요.", "dad": "출산 후 육아 분담 계획을 미리 이야기해 두세요.", "caution": "전치태반, 태아 위치 이상은 이 시기에 재확인"},
    35: {"size": "허니듀 멜론 (460mm)", "fetal": "대부분의 장기가 완성됐어요. 이제 살이 오르는 단계예요.", "mom": "골반 압통, 좌골 신경통이 심해질 수 있어요.", "dad": "산후조리원 or 집 산후 계획을 확정하세요.", "caution": "GBS(B군 연쇄구균) 검사 시기 (35~37주)"},
    36: {"size": "파파야 (470mm)", "fetal": "머리가 골반 아래로 내려오기 시작해요.", "mom": "숨이 갑자기 편해질 수 있어요—아기가 내려온 거예요!", "dad": "진통이 시작되면 가야 할 병원과 연락처를 재확인하세요.", "caution": "주 1회 정기검진 시작. 이슬·파수·규칙적 진통 주의"},
    37: {"size": "겨울 멜론 (480mm)", "fetal": "만삭 초기! 모든 장기가 완성됐어요. 언제 나와도 건강해요.", "mom": "진통이 언제 올지 모르니 항상 가방을 챙겨 두세요.", "dad": "아내 곁을 자주 지켜주세요. 혼자 두지 마세요.", "caution": "파수(양수가 흘러내림) 시 즉시 병원 방문—누워서 이동"},
    38: {"size": "리크 (482mm)", "fetal": "손발톱이 손끝·발끝을 지나쳐요. 머리카락이 자랐어요!", "mom": "자궁경부가 열리고 얇아지는 중이에요.", "dad": "진통 타이밍을 재는 앱을 핸드폰에 설치해 두세요.", "caution": "진통 간격 10분→5분→규칙적으로 강해지면 병원 출발"},
    39: {"size": "미니 수박 (495mm)", "fetal": "뇌·신경계가 계속 발달해요. 출산 준비 완료 상태입니다!", "mom": "불안하고 긴장될 수 있어요. 충분히 쉬세요.", "dad": "진진통 신호를 완벽히 숙지하고, 항상 대기 상태를 유지하세요.", "caution": "태동이 현저히 줄면 즉시 병원—절대 기다리지 마세요"},
    40: {"size": "작은 수박 (510mm)", "fetal": "D-Day! 이레가 세상에 나올 준비가 됐어요 💖", "mom": "기다림 자체가 힘들지만, 만남이 코앞이에요!", "dad": "아내 손을 꼭 잡고 함께해 주세요. 당신이 최고의 선물이에요.", "caution": "41주 초과 시 유도분만 검토—주치의 지시에 따르세요"},
}

# ==========================================
# 검사 일정 데이터
# ==========================================
EXAM_SCHEDULE = [
    {"period": "4~8주", "exams": [
        {"name": "초기 임신 확인 초음파", "type": "필수", "desc": "자궁 내 착상 확인, 심박동 확인"},
        {"name": "혈액검사 (기본)", "type": "필수", "desc": "혈액형, 빈혈, 풍진 항체, B형·C형 간염, 매독, HIV 등"},
        {"name": "소변검사", "type": "필수", "desc": "단백뇨, 당뇨, 요로감염 확인"},
        {"name": "자궁경부암 검사", "type": "필수", "desc": "임신 초기 1회 시행"},
        {"name": "엽산 복용 시작", "type": "권고", "desc": "신경관 결손 예방 (400~800㎍/일)"},
    ]},
    {"period": "10~13주", "exams": [
        {"name": "NT 초음파 (목덜미 투명대)", "type": "필수", "desc": "다운증후군 등 염색체 이상 선별"},
        {"name": "1차 통합 선별검사", "type": "필수", "desc": "혈액검사+NT 초음파 조합. 11~13+6주 시행"},
        {"name": "비침습적 산전 검사 (NIPT)", "type": "선택", "desc": "산모 혈액으로 염색체 이상 정밀 확인. 비급여"},
        {"name": "융모막 융모 생검 (CVS)", "type": "고위험군", "desc": "염색체 이상 확진 검사. 고위험군만"},
    ]},
    {"period": "15~20주", "exams": [
        {"name": "2차 통합 선별검사 (쿼드 검사)", "type": "필수", "desc": "신경관 결손, 다운증후군, 18삼체성 선별. 15~20주"},
        {"name": "정밀 초음파 (대형 기형아 검사)", "type": "필수", "desc": "태아 구조 이상 여부 정밀 확인. 18~20주 최적"},
        {"name": "양수 검사", "type": "고위험군", "desc": "선별검사 이상 또는 고령 산모 염색체 확진"},
    ]},
    {"period": "24~28주", "exams": [
        {"name": "임신성 당뇨 선별검사 (GCT)", "type": "필수", "desc": "50g 포도당 음료 복용 후 1시간 혈당 측정"},
        {"name": "임신성 당뇨 확진검사 (GTT)", "type": "GCT 이상 시", "desc": "100g 포도당 3시간 검사"},
        {"name": "빈혈 검사", "type": "필수", "desc": "철분 결핍성 빈혈 확인. 필요 시 철분제 처방"},
        {"name": "정기 초음파", "type": "필수", "desc": "태아 성장 속도·위치·양수량 확인"},
    ]},
    {"period": "28~32주", "exams": [
        {"name": "정기 초음파", "type": "필수", "desc": "2주마다 성장·위치 확인"},
        {"name": "태아 심음 모니터링(NST)", "type": "필요시", "desc": "태아 안녕 확인. 고위험 임신부는 정기적으로"},
        {"name": "조기 진통 확인", "type": "증상시", "desc": "규칙적 배뭉침·출혈·이상 분비물 시 즉시 내원"},
    ]},
    {"period": "35~37주", "exams": [
        {"name": "B군 연쇄구균(GBS) 검사", "type": "필수", "desc": "질·직장 배양 검사. 양성 시 분만 중 항생제 투여"},
        {"name": "태아 위치 확인", "type": "필수", "desc": "역아 시 외회전술 또는 제왕절개 계획"},
        {"name": "자궁경부 숙화 평가", "type": "필수", "desc": "유도분만 필요 여부 확인"},
    ]},
    {"period": "36~40주", "exams": [
        {"name": "주 1회 정기 검진", "type": "필수", "desc": "자궁경부 개대·소실, 태아 하강도 확인"},
        {"name": "태동 모니터링", "type": "자가 체크", "desc": "하루 2시간 안에 10회 이상 느껴지면 정상"},
        {"name": "비자극 검사(NST)", "type": "필요시", "desc": "태동 감소 등 이상 시 즉시 시행"},
        {"name": "41주 초과 시 유도분만 검토", "type": "필수", "desc": "주치의 지시에 따라 결정"},
    ]},
]

# ==========================================
# 음식 안전 가이드 데이터
# (수은 관련 분류는 식약처 '임신·수유 여성 생선 안전 섭취 가이드' 기준 참고)
# ==========================================
FOOD_GUIDE = {
    "단백질·육류": [
        {"name": "완전히 익힌 고기류", "status": "ok", "reason": "임신 중 철분·단백질의 주요 공급원"},
        {"name": "날고기(육회, 스테이크 레어)", "status": "no", "reason": "리스테리아·살모넬라·톡소플라즈마 감염 위험"},
        {"name": "가공육(소시지, 햄)", "status": "warn", "reason": "나트륨·방부제 과다. 완전히 익혀서 소량만"},
        {"name": "닭고기 (완전히 익힌 것)", "status": "ok", "reason": "저지방 고단백. 반드시 완전히 익힐 것"},
    ],
    "해산물·생선": [
        {"name": "오메가3 풍부 생선(고등어·연어 익힌 것)", "status": "ok", "reason": "태아 뇌 발달에 필수적인 DHA 공급. 일반어류는 주 2~3회 수준 권장"},
        {"name": "생선회·초밥", "status": "no", "reason": "리스테리아·기생충 감염 위험"},
        {"name": "참치 통조림", "status": "warn", "reason": "수은 함량—주 1~2캔 이하 (최신 권장량은 식약처 가이드 확인)"},
        {"name": "상어·황새치·참다랑어 등 심해성 어류", "status": "no", "reason": "메틸수은 함량 높음—섭취 제한 대상"},
        {"name": "새우·조개 (완전히 익힌 것)", "status": "ok", "reason": "저지방 단백질 공급"},
        {"name": "굴·조개 생것", "status": "no", "reason": "비브리오·노로바이러스 감염 위험"},
    ],
    "유제품·달걀": [
        {"name": "저온 살균 우유·치즈", "status": "ok", "reason": "칼슘과 단백질의 좋은 공급원"},
        {"name": "비살균 생유·소프트 치즈(브리·카망베르·페타)", "status": "no", "reason": "리스테리아 감염 위험"},
        {"name": "완전히 익힌 달걀", "status": "ok", "reason": "단백질·콜린 공급. 완전히 익혀야 함"},
        {"name": "반숙·날달걀(에그노그 등)", "status": "no", "reason": "살모넬라 감염 위험"},
        {"name": "요거트(저온살균)", "status": "ok", "reason": "칼슘·프로바이오틱스 공급"},
    ],
    "채소·과일": [
        {"name": "잘 씻은 신선 채소·과일", "status": "ok", "reason": "비타민·식이섬유·엽산 공급"},
        {"name": "발아채소(새싹채소)", "status": "warn", "reason": "살모넬라 위험—익혀서 먹거나 주의"},
        {"name": "파파야 (덜 익은 것)", "status": "no", "reason": "파파인 성분이 자궁 수축 유발 가능"},
        {"name": "파인애플 (과량)", "status": "warn", "reason": "브로멜라인 성분—소량은 괜찮음"},
        {"name": "시금치·브로콜리·고구마", "status": "ok", "reason": "철분·칼슘·엽산·비타민A 풍부"},
    ],
    "음료·기호식품": [
        {"name": "물 (하루 2L 이상)", "status": "ok", "reason": "양수 유지, 변비 예방, 혈액순환에 필수"},
        {"name": "커피 (하루 1잔 이하, 200mg 이하)", "status": "warn", "reason": "카페인 과다 시 유산·저체중아 위험"},
        {"name": "술(모든 종류)", "status": "no", "reason": "태아 알코올 증후군—안전한 양은 없음"},
        {"name": "에너지 드링크", "status": "no", "reason": "고카페인+타우린 등 성분 위험"},
        {"name": "녹차·홍차 (하루 1~2잔)", "status": "warn", "reason": "카페인 함유—소량만"},
        {"name": "허브티 (생강차·루이보스)", "status": "ok", "reason": "카페인 없고 입덧 완화에 도움"},
    ],
    "기타 주의 식품": [
        {"name": "리코리스(감초)", "status": "no", "reason": "조기 진통 유발 가능성"},
        {"name": "알로에베라 (내복)", "status": "no", "reason": "자궁 수축 성분 포함"},
        {"name": "간(소·돼지)", "status": "warn", "reason": "비타민A 과다—가끔 소량만"},
        {"name": "인스턴트 식품", "status": "warn", "reason": "나트륨 과다—부종 악화. 최소화"},
        {"name": "견과류", "status": "ok", "reason": "오메가3·비타민E 풍부. 알레르기 없다면 추천"},
    ],
}

# ==========================================
# 💊 약물 안전 가이드 (NEW)
# ※ 아래 분류는 일반적으로 알려진 정보이며, 실제 복용은
#   반드시 산부인과 전문의·약사 또는 마더세이프(1588-7309) 상담 후 결정하세요.
# ==========================================
DRUG_GUIDE = {
    "해열·진통제": [
        {"name": "아세트아미노펜 (타이레놀)", "status": "ok", "reason": "임신 중 해열·진통에 일반적으로 우선 고려되는 성분. 단, 권장 용량 내 단기 사용 원칙이며 복용 전 의사·약사 확인"},
        {"name": "이부프로펜·NSAIDs (부루펜 등)", "status": "no", "reason": "특히 임신 20주 이후 태아 신장·양수량에 영향 가능성으로 사용 제한 권고. 임신 중 전 기간 자가 복용 금지"},
        {"name": "아스피린", "status": "warn", "reason": "저용량은 특정 고위험 산모에게 의사가 처방하는 경우가 있으나, 자가 판단 복용은 금지"},
    ],
    "감기·알레르기": [
        {"name": "일부 항히스타민제 (클로르페니라민 등)", "status": "warn", "reason": "비교적 오래 사용된 성분이지만 제품·시기별로 다르므로 반드시 약사·의사 확인 후"},
        {"name": "코감기약 (슈도에페드린 등 혈관수축제)", "status": "warn", "reason": "임신 초기에는 특히 주의. 의사 상담 없이 복용하지 않기"},
        {"name": "종합감기약", "status": "warn", "reason": "여러 성분 복합—성분별 안전성이 다르므로 단일 성분 약을 상담 후 선택하는 것이 원칙"},
        {"name": "생리식염수 코세척·가습", "status": "ok", "reason": "약물 아닌 비약물 요법—코막힘 완화에 안전하게 사용 가능"},
    ],
    "소화기": [
        {"name": "제산제 (알긴산·수산화마그네슘 계열)", "status": "warn", "reason": "속쓰림에 흔히 사용되나 성분별 차이 있음—약사에게 '임신 중'임을 알리고 선택"},
        {"name": "변비약 (차전자피 등 팽창성)", "status": "ok", "reason": "식이섬유 계열은 비교적 안전한 편. 자극성 변비약은 상담 후"},
        {"name": "자극성 변비약 (비사코딜 등)", "status": "warn", "reason": "장기간·과량 사용 주의. 식이·수분 개선이 우선"},
        {"name": "유산균 (프로바이오틱스)", "status": "ok", "reason": "일반적으로 사용 가능. 제품 성분 확인"},
    ],
    "항생제 (처방 시)": [
        {"name": "페니실린·아목시실린 계열", "status": "ok", "reason": "의사 처방 하에 임신 중 비교적 안전하게 사용되는 계열"},
        {"name": "세팔로스포린 계열", "status": "ok", "reason": "의사 처방 하에 사용 가능한 계열"},
        {"name": "테트라사이클린 계열", "status": "no", "reason": "태아 치아·뼈 발달에 영향—임신 중 금기"},
        {"name": "퀴놀론 계열 (시프로플록사신 등)", "status": "no", "reason": "임신 중 일반적으로 사용하지 않는 계열"},
    ],
    "피부·기타": [
        {"name": "이소트레티노인 (여드름약, 로아큐탄 등)", "status": "no", "reason": "심각한 기형 유발—임신 중 절대 금기. 복용 중이었다면 즉시 의사 상담"},
        {"name": "스테로이드 연고 (약한 등급, 소량)", "status": "warn", "reason": "부위·기간에 따라 다름—의사 처방·지시에 따라"},
        {"name": "경구 무좀약·항진균제", "status": "warn", "reason": "성분별 차이 큼—반드시 의사 상담"},
        {"name": "한약·건강기능식품", "status": "warn", "reason": "'천연'이 안전을 의미하지 않음—성분 확인 후 전문가 상담 필수"},
    ],
}

# ==========================================
# 🚨 응급 상황 행동 플로우 (NEW)
# ==========================================
EMERGENCY_FLOW = [
    {
        "title": "🌊 파수 (양수가 흘러내림)",
        "urgency": "즉시 병원",
        "steps": [
            "당황하지 말고 패드(또는 큰 수건)를 대세요",
            "샤워·탕목욕 하지 마세요 (감염 위험)",
            "가능한 눕거나 비스듬히 기대어 이동 준비",
            "병원에 전화해 파수 사실과 도착 예정 시간을 알리세요",
            "양수 색이 초록·갈색이면 반드시 병원에 미리 말하세요",
        ],
    },
    {
        "title": "⏱️ 규칙적인 진통",
        "urgency": "간격 확인 후 병원",
        "steps": [
            "아래 배뭉침 타이머로 간격·지속시간을 기록하세요",
            "초산: 5분 간격 규칙적 진통이 1시간 지속되면 병원 출발 (병원 지침 우선)",
            "경산: 진행이 빠를 수 있으니 10분 간격부터 병원과 상의",
            "출산 가방·서류 챙기고, 이동 중 아내를 혼자 두지 마세요",
        ],
    },
    {
        "title": "🩸 질 출혈",
        "urgency": "양에 따라 판단",
        "steps": [
            "만삭 전후 소량의 피 섞인 점액(이슬)은 출산이 가까워진 신호일 수 있어요",
            "생리처럼 흐르는 선홍색 출혈은 즉시 병원 — 절대 기다리지 마세요",
            "출혈 + 복통 동반 시 응급실로 바로 이동",
        ],
    },
    {
        "title": "👶 태동 감소",
        "urgency": "2시간 기준 확인",
        "steps": [
            "왼쪽으로 누워 조용한 곳에서 태동을 세어보세요",
            "간식·찬 물을 마신 후 다시 확인해 보세요",
            "2시간 동안 10회 미만이면 즉시 병원에 연락 — 기다리지 마세요",
        ],
    },
    {
        "title": "🤕 심한 두통·시야 이상·윗배 통증",
        "urgency": "즉시 병원 (전자간증 의심)",
        "steps": [
            "갑작스러운 심한 두통, 눈앞이 번쩍이거나 흐려짐, 오른쪽 윗배 통증, 갑작스런 부종은 임신중독증(전자간증) 신호일 수 있어요",
            "혈압을 잴 수 있으면 측정하고, 즉시 병원에 연락하세요",
            "자가 진통제 복용으로 버티지 마세요",
        ],
    },
    {
        "title": "🌡️ 38도 이상 고열",
        "urgency": "당일 진료",
        "steps": [
            "체온을 기록하고 병원에 연락하세요",
            "해열은 의사·약사 상담 후 (일반적으로 아세트아미노펜이 우선 고려되나 자가 판단 금지)",
            "고열 + 배뭉침·분비물 이상 동반 시 즉시 내원",
        ],
    },
]

# ==========================================
# 🎉 마일스톤 (NEW) — 주차 기준
# ==========================================
MILESTONES = [
    (12, "1차 기형아 검사 마감 주간"),
    (13, "안정기 진입 🎉"),
    (20, "임신 절반! 정밀 초음파 시기"),
    (24, "임신성 당뇨 검사 시작"),
    (28, "3분기 시작 — 검진 2주 간격"),
    (34, "조산 시에도 생존율이 크게 높아지는 시기"),
    (35, "GBS 검사 · 출산 가방 완성 목표"),
    (37, "만삭 진입 🎉"),
    (40, "출산 예정일 💖"),
]

# ==========================================
# 🏛️ 정부 지원·행정 절차 (NEW)
# ※ 지원 금액·조건은 매년 변경됩니다. 반드시 정부24·복지로에서 최신 기준을 확인하세요.
# ==========================================
GOV_SUPPORT = [
    {"name": "임신·출산 진료비 지원 (국민행복카드)", "when": "임신 확인 직후", "how": "산부인과에서 임신확인서 발급 → 카드사·복지로 신청", "note": "진료비·약제비 바우처. 다태아는 지원액 상이"},
    {"name": "맘편한 임신 원스톱 서비스", "when": "임신 확인 후", "how": "정부24에서 임신 관련 지원을 한 번에 통합 신청", "note": "엽산·철분제, 교통비(일부 지자체) 등 포함"},
    {"name": "첫만남이용권", "when": "출생 후", "how": "출생신고 시 행정복지센터 또는 복지로에서 신청", "note": "출생아 대상 바우처 — 금액은 복지로에서 확인"},
    {"name": "부모급여 / 아동수당", "when": "출생 후 60일 이내 신청 권장", "how": "행정복지센터 또는 복지로", "note": "출생일 기준 소급 지급 조건이 있어 60일 내 신청이 유리"},
    {"name": "출생신고", "when": "출생 후 1개월 이내 (법정 기한)", "how": "주소지 행정복지센터 또는 온라인(대법원 전자가족관계등록시스템)", "note": "병원 출생증명서 필요. 기한 경과 시 과태료"},
    {"name": "산모·신생아 건강관리 지원 (산후도우미)", "when": "출산예정일 40일 전 ~ 출산 후 30일", "how": "보건소 또는 복지로 신청", "note": "소득 기준·지자체별 확대 여부 확인 필요"},
    {"name": "지자체 출산지원금·축하용품", "when": "지자체별 상이", "how": "거주지 시·군·구청 홈페이지 확인", "note": "지역별 차이가 크므로 거주지 기준 확인"},
    {"name": "직장인: 출산휴가·배우자 출산휴가·육아휴직", "when": "출산 전후", "how": "회사 인사팀 + 고용보험 (고용24)", "note": "급여 지원 조건·기간은 고용노동부 최신 기준 확인"},
]

# ==========================================
# 👨‍👩‍👧 출산휴가·육아휴직 제도 데이터 (NEW)
# ※ 2026-07 기준. 급여 상한액은 '출산전후휴가 급여등 상한액 고시'(고용노동부 고시,
#   2026.1.1 시행) 및 고용보험법령 기준. 매년 변경되므로 고용24(work24.go.kr)에서
#   최신 기준·모의계산 확인 필수. 회사 취업규칙에 법정 기준 이상의 규정이 있을 수 있음.
# ==========================================
LEAVE_RULES = {
    "출산전후휴가": {
        "총일수": {"단태아": 90, "다태아": 120, "미숙아": 100},
        "출산후최소": {"단태아": 45, "다태아": 60, "미숙아": 45},
        "유급일수": {"단태아": 60, "다태아": 75, "미숙아": 60},  # 사업주 유급 의무 구간
        "급여상한_총액": {"단태아": 6_600_000, "다태아": 8_800_000, "미숙아": 7_333_330},  # 2026년 고시
        "비고": "역일(달력일) 기준. 우선지원대상기업은 전체 기간 고용보험 지원, 대규모 기업은 마지막 30일(다태아 45일)만 지원",
    },
    "배우자출산휴가": {
        "일수": 20,           # 근무일 기준 (주말·공휴일 제외)
        "사용기한_일": 120,   # 출산일부터 120일 이내
        "분할횟수": 3,        # 3회 분할 = 4개 구간
        "급여상한_20일": 1_684_210,  # 2026년 고시, 우선지원대상기업 근로자 대상
    },
    "육아휴직": {
        "기본_개월": 12,
        "연장_개월": 18,      # 부모 각 3개월+ 사용 / 한부모 / 중증장애아동 부모
        "분할횟수": 3,        # 3회 분할 = 4개 구간
        # 월별 급여: (지급률, 상한액) — 1~3개월 100%/250만, 4~6개월 100%/200만, 7개월~ 80%/160만
        "급여구간": [(3, 1.00, 2_500_000), (6, 1.00, 2_000_000), (18, 0.80, 1_600_000)],
        "하한": 700_000,
        # 6+6 부모육아휴직제: 생후 18개월 내 부모 모두 사용 시 첫 6개월 월별 상한 (각자)
        "육육상한": [2_500_000, 2_500_000, 3_000_000, 3_500_000, 4_000_000, 4_500_000],
    },
}

LEAVE_SUMMARY = [
    {"name": "🤱 출산전후휴가", "who": "출산한 엄마 (근로기준법상 권리)", "period": "90일 (다태아 120일 · 미숙아 100일)",
     "point": "출산 후 45일 이상(다태아 60일) 반드시 확보 · 역일 기준 · 최초 60일(다태아 75일)은 사업주 유급 의무",
     "pay": "우선지원대상기업: 90일 전체 고용보험 지원 (2026년 총 상한 660만원) / 대규모 기업: 마지막 30일만 지원",
     "apply": "휴가 시작 1개월 후~종료 후 12개월 이내 고용24 신청 (고용보험 180일 이상)"},
    {"name": "👨 배우자 출산휴가", "who": "출산한 배우자를 둔 아빠", "period": "20일 (근무일 기준 — 주말·공휴일 제외)",
     "point": "출산일부터 120일 이내 사용 · 3회 분할 가능(4구간) · 미부여 사업주 과태료 500만원",
     "pay": "우선지원대상기업: 20일 전체 고용보험 지원 (2026년 상한 1,684,210원, 초과분 사업주 부담) / 대규모: 사업주 전액 유급",
     "apply": "휴가 시작 1개월 후~종료 후 12개월 이내 고용24 신청 (고용보험 180일 이상)"},
    {"name": "👶 육아휴직", "who": "엄마·아빠 각각 (임신 중에도 가능)", "period": "기본 1년 → 조건 충족 시 1년 6개월",
     "point": "연장 조건: 부모 모두 같은 자녀에 각 3개월 이상 사용 / 한부모 / 중증장애아동 부모 · 3회 분할(4구간) · 시작 30일 전 회사에 신청",
     "pay": "1~3개월 통상임금 100%(상한 250만) · 4~6개월 100%(상한 200만) · 7개월~ 80%(상한 160만) · 사후지급금 폐지(전액 즉시 지급)",
     "apply": "회사에 신청서 제출 → 회사가 고용24에 확인서 등록 → 본인이 고용24에서 급여 신청"},
    {"name": "⏰ 육아기 근로시간 단축", "who": "만 12세(초6) 이하 자녀를 둔 근로자", "period": "최대 36개월 (미사용 육아휴직 기간 2배 가산 전환 가능)",
     "point": "주 15~35시간으로 단축 · 휴직이 부담스러울 때 대안",
     "pay": "최초 주 10시간 단축분 통상임금 100% (2026년 상한 월 250만원) · 나머지 단축분 80% (상한 160만원)",
     "apply": "회사 신청 → 고용24 급여 신청"},
]

# ==========================================
# 육아 가이드 데이터 (0~24개월)
# ==========================================
BABY_CARE = [
    {
        "range": "0~1개월 (신생아)",
        "color": "card-purple",
        "title_color": "card-title-purple",
        "development": "시력은 20~30cm 거리만 인식해요. 엄마·아빠 얼굴을 바라봐요. 원시 반사(빨기, 잡기, 모로 반사)가 있어요.",
        "feeding": "모유 또는 분유를 2~3시간마다 수유해요. 하루 8~12회가 정상이에요.",
        "sleep": "하루 16~18시간 수면. 낮밤 구분이 없어요.",
        "milestones": ["고개를 잠깐 들 수 있어요", "소리에 반응해요", "울음으로 의사 표현"],
        "care": "목욕은 매일 할 필요 없어요. 얼굴·목·엉덩이 위주로. 배꼽이 떨어질 때까지 통목욕 금지.",
        "caution": "절대 흔들지 마세요(흔들린 아이 증후군). 모든 예방접종 일정을 지켜주세요.",
    },
    {
        "range": "2~3개월",
        "color": "card-teal",
        "title_color": "card-title-teal",
        "development": "사회적 미소가 나타나요! 눈으로 물체를 따라봐요. 소리를 내기 시작해요(쿠잉).",
        "feeding": "모유/분유 3~4시간 간격으로 줄어들 수 있어요.",
        "sleep": "하루 14~16시간. 밤 수유가 2~3회 필요해요.",
        "milestones": ["사회적 미소(꼭 찍어두세요!)", "배밀이 자세에서 고개 들기", "소리에 고개 돌리기"],
        "care": "터미 타임(배 엎드리기) 하루 여러 번, 1~2분씩 연습해요.",
        "caution": "예방접종: B형간염, 뇌수막염(Hib), 폐렴구균, DTaP, 소아마비 등 — 일정은 예방접종도우미 확인",
    },
    {
        "range": "4~6개월",
        "color": "card-blue",
        "title_color": "card-title-blue",
        "development": "뒤집기를 시작해요! 물건을 잡고 입으로 가져가요. 이유식 준비가 됩니다.",
        "feeding": "이유식은 보통 생후 4~6개월 사이 시작. 쌀미음부터 시작해 한 가지씩 추가해요.",
        "sleep": "밤 수면이 길어져요. 6개월이면 6~8시간 연속 수면이 가능해요.",
        "milestones": ["뒤집기 (앞→뒤, 뒤→앞)", "양손으로 물건 잡기", "자기 이름에 반응"],
        "care": "이유식은 쌀미음→채소 퓨레→과일 퓨레 순서. 알레르기 식품은 4~5일 간격으로 하나씩.",
        "caution": "꿀은 만 1세 전 절대 금지(보툴리눔독소). 소금·설탕 첨가 금지.",
    },
    {
        "range": "7~9개월",
        "color": "card-green",
        "title_color": "card-title-green",
        "development": "기어다니기 시작! 낯가림이 생겨요. '엄마', '아빠' 옹알이를 해요.",
        "feeding": "이유식 하루 2회. 으깬 연두부·계란 노른자 등 다양한 식재료 도전.",
        "sleep": "하루 14시간. 낮잠 2회(오전·오후).",
        "milestones": ["배밀이·기기 시작", "혼자 앉기", "낯가림 시작"],
        "care": "집안 안전 점검! 계단 안전문, 콘센트 커버, 서랍 잠금 장치 설치.",
        "caution": "이물질 삼킴 사고 주의. 작은 물건을 손에 닿지 않게 해주세요.",
    },
    {
        "range": "10~12개월",
        "color": "card-orange",
        "title_color": "card-title-orange",
        "development": "붙잡고 일어서기! 첫 걸음마를 뗄 수 있어요. 간단한 지시를 이해해요.",
        "feeding": "이유식 하루 3회. 거의 가족 식사와 비슷한 형태의 연식으로 전환.",
        "sleep": "밤 10~12시간 + 낮잠 1~2회.",
        "milestones": ["붙잡고 서기·걷기", "엄마·아빠 구별해 부르기", "짝짜꿍·빠이빠이"],
        "care": "첫 생일 이후 우유를 시작해요(하루 400~500mL). 젖병보다 컵 사용을 연습.",
        "caution": "걸음마 시작 후 낙상 사고 주의. 모서리 보호대 부착.",
    },
    {
        "range": "13~18개월",
        "color": "card-purple",
        "title_color": "card-title-purple",
        "development": "혼자 걷기 시작! 10~20개 단어를 말해요. 가리키기로 의사 표현.",
        "feeding": "가족 식사와 동일한 음식 가능. 씹기 쉬운 형태로 제공.",
        "sleep": "밤 11~12시간 + 낮잠 1회(1~2시간).",
        "milestones": ["혼자 걷기", "단어 10~20개", "숟가락 사용 시도"],
        "care": "그림책을 많이 읽어주세요. 어휘 발달에 큰 도움이 돼요.",
        "caution": "18개월까지 단어 없으면 언어 발달 평가 권장. 스마트폰 노출 최소화.",
    },
    {
        "range": "19~24개월",
        "color": "card-teal",
        "title_color": "card-title-teal",
        "development": "두 단어 연결(엄마 줘, 아빠 안아). 계단 오르기, 뛰기. 또래 친구에 관심을 가져요.",
        "feeding": "편식이 시작될 수 있어요. 억지로 먹이지 말고 다양하게 제공해요.",
        "sleep": "밤 11시간 + 낮잠 1회.",
        "milestones": ["두 단어 이상 연결", "달리기·점프", "소꿉놀이·모방 놀이"],
        "care": "규칙적인 일과(식사·수면·놀이)가 아이에게 안정감을 줘요.",
        "caution": "2세까지 스마트폰·TV 노출을 제한하는 것이 발달에 좋아요. (WHO 권고)",
    },
]

# ==========================================
# 예방접종 스케줄
# ※ 표준 예방접종 일정은 변경될 수 있으니 질병관리청 '예방접종도우미'에서 최신 일정을 확인하세요.
# ==========================================
VACCINATION = [
    {"age": "출생 시", "vaccines": ["B형 간염 1차", "BCG (생후 4주 이내)"]},
    {"age": "1개월", "vaccines": ["B형 간염 2차"]},
    {"age": "2개월", "vaccines": ["DTaP 1차", "폴리오(IPV) 1차", "뇌수막염(Hib) 1차", "폐렴구균(PCV) 1차", "로타바이러스 1차"]},
    {"age": "4개월", "vaccines": ["DTaP 2차", "폴리오(IPV) 2차", "Hib 2차", "PCV 2차", "로타바이러스 2차"]},
    {"age": "6개월", "vaccines": ["DTaP 3차", "폴리오(IPV) 3차", "Hib 3차", "PCV 3차", "B형 간염 3차", "인플루엔자(매년)"]},
    {"age": "12~15개월", "vaccines": ["MMR 1차", "수두 1차", "Hib 4차", "PCV 4차", "A형 간염 1차"]},
    {"age": "12~23개월", "vaccines": ["일본뇌염 1·2차 (불활성화 백신 기준)"]},
    {"age": "15~18개월", "vaccines": ["DTaP 4차", "A형 간염 2차 (1차 후 6개월 이상 간격)"]},
    {"age": "4~6세", "vaccines": ["DTaP 5차", "폴리오 4차", "MMR 2차", "수두 2차"]},
]

# ==========================================
# 출산 준비물 체크리스트
# ==========================================
CHECKLIST = {
    "👗 엄마 준비물": [
        "산모패드 2팩 — 아브리산 추천 (오로가 한 달간 나와 생리대로는 부족해요)",
        "회음부 방석 1개 (자연분만 시 회음부 절개 후 필수)",
        "수유브라·나시 2~3개 (모유수유 시 필수)",
        "수유패드 한팩 (모유·분유 확인 후 추가 구매)",
        "유두보호기·쭈쭈젖꼭지 (편평·함몰유두 시 사용, 아기 빠는 힘 세지면 자연 수유)",
    ],
    "👶 아기 의류·침구": [
        "배냇저고리 2~4개",
        "배냇슈트 2~3개 (외출 시 편리 — 밑 똑딱이만 열면 기저귀 교체 OK)",
        "속싸개 2개 (한 달 후 스와들미·스와들업으로 교체)",
        "겉싸개 1개",
        "내복 (선물로 들어오기도 함, 몇 개 미리 준비)",
        "손발목 보호대 1세트 — 마더스베이비 추천 (손목 아대형, 손 끼우는 형 말고)",
        "방수요 2개 (기저귀 교체 시 소변·대변 테러 방지)",
        "면손수건 40~50개",
        "가제손수건 30개",
        "지퍼백 (아기 옷·손수건 삶은 후 보관용)",
    ],
    "🍼 수유·영양": [
        "젖병 2~3개 (분유 또는 유축 시 모두 필요)",
        "젖병소독기 (모유수유 시도 있으면 편리한 만능 아이템)",
        "젖병솔·젖꼭지솔",
        "젖병세정제",
        "모유저장팩 (유축 후 냉동 보관용)",
        "역류방지쿠션 — 제이앤제나 추천",
    ],
    "🛁 위생·건강": [
        "슈너글 아기욕조 (헹굼용 대야도 함께 준비)",
        "손세정제 — 아이깨끗해 추천",
        "물티슈 1박스 — 베베숲 추천 (도톰하고 물기 충분, 가성비 좋음)",
        "기저귀 신생아용·소형 각 1팩 — 팸퍼스 추천 (금방금방 씀)",
        "발진크림 — 비판텐 추천 (기저귀발진·작은 상처에도 만능)",
        "체온계 — 브라운 추천",
        "온도습도계 — 드렉텍 추천",
        "배꼽소독솜 (약국에서 구매 — 알콜+집게 세트로 줌)",
        "애기로션·바스·오일",
        "아기면봉 (귀 파는 용 아님, 목욕 후 물기 제거용)",
        "손톱가위 3종 세트 — 마더케이 추천",
        "세탁세제·유연제·비누 — 비앤비 추천 (세탁비누는 응가 얼룩 제거용)",
        "피지오머 베이비 or 마플러스 나잘스프레이 (코막힘 완화)",
        "노시부 or 코끼리뻥코 (아기 코 흡인기 — 어른도 사용 가능, 일찍 살수록 이득)",
    ],
    "🎪 장난감·발달": [
        "딸랑이 1세트 (파스텔 말고 원색·단색 — 아기가 더 잘 가지고 놀아요)",
        "초점책 1개 (직접 만들거나 구매, 조리원 프로그램에서 만들기도 함)",
        "모빌 흑백·컬러 — 타이니러브 추천 (신생아 때부터 사용 가능)",
        "수유등 (쿠팡에 예쁜 것 많음)",
    ],
    "🎒 외출·이동": [
        "기저귀가방 (종류 많으니 본인에게 편한 것으로)",
        "아기띠+힙시트 세트 (힙시트는 허리 힘 생기면 사용, 슬링은 신생아 보조용)",
        "카시트 (퇴원 시 필수!)",
    ],
    "📋 서류·기타": [
        "산모 수첩",
        "신분증 (산모·배우자)",
        "건강보험증",
        "병원 예약 확인서",
        "현금 (만일 대비)",
        "카메라·핸드폰 충전기 및 보조배터리",
        "출생신고 준비 메모",
    ],
}

# ==========================================
# 시간 계산 (KST)
# ==========================================
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
today_date = now.date()

# ==========================================
# 사이드바
# ==========================================
with st.sidebar:
    st.markdown('<span class="sidebar-title">💖 이레 안심 가이드</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="sidebar-today">{now.strftime("%Y년 %m월 %d일")} ({["월","화","수","목","금","토","일"][now.weekday()]})</span>', unsafe_allow_html=True)

    day_index = (now.day - 1) % len(bible_list)
    verse, ref = bible_list[day_index]
    st.markdown(f'<div class="bible-box">"{verse}"<span class="bible-ref">— {ref} —</span></div>', unsafe_allow_html=True)

    lmp_date = st.date_input("마지막 생리 시작일(LMP)", datetime(2026, 3, 15).date())
    due_date = lmp_date + timedelta(days=280)
    total_days = max(0, (today_date - lmp_date).days)
    current_weeks, current_days_rem = total_days // 7, total_days % 7
    d_day = (due_date - today_date).days
    baby_mode = d_day <= 0  # 출산 예정일 이후엔 육아 모드

    st.markdown(f"""
    <div class="sb-box">
        <span style="color:#888; font-size:0.85rem;">우리 이레는 지금</span><br>
        <span style="font-size:1.9rem; font-weight:900; color:#ff4757;">{current_weeks}주 {current_days_rem}일차</span><br>
        <b style="color:#ff6b6b; font-size:1.2rem;">{"D-Day! 🎉" if d_day <= 0 else f"D-{d_day}"}</b><br>
        <span style="font-size:0.8rem; color:#aaa;">예정일: {due_date.strftime("%Y.%m.%d")}</span>
    </div>
    """, unsafe_allow_html=True)

    # 🎉 다가오는 마일스톤 (NEW)
    upcoming = [(w, label) for (w, label) in MILESTONES if w > current_weeks][:2]
    if not baby_mode and upcoming:
        st.markdown("**🎉 다가오는 기념일**")
        for w, label in upcoming:
            m_date = lmp_date + timedelta(weeks=w)
            dd = (m_date - today_date).days
            st.markdown(f'<div class="milestone-box"><b>D-{dd}</b> · {w}주차<br>{label}</div>', unsafe_allow_html=True)
    if not baby_mode and 0 < d_day <= 100 and d_day % 10 == 0:
        st.balloons()

    with st.expander("🌡️ 오늘 엄마 컨디션 기록"):
        cond = st.select_slider("상태", options=["힘듦", "보통", "좋음"], key="cs", label_visibility="collapsed")
        memo = st.text_input("메모", key="cm", placeholder="아빠에게 한마디")
        if st.button("기록 전송"):
            if save_to_sheets("컨디션", memo, cond):
                st.toast("기록 완료! ❤️")

    with st.expander("💌 태교 편지함"):
        letter = st.text_area("이레에게...", key="la", placeholder="오늘의 기록을 남겨보세요")
        if st.button("편지 저장"):
            if save_to_sheets("태교편지", letter):
                st.success("저장 완료! ❤️")

    with st.expander("👶 태동 카운터"):
        if "kick_count" not in st.session_state:
            st.session_state.kick_count = 0
        if "kick_start" not in st.session_state:
            st.session_state.kick_start = now
        elapsed_min = int((now - st.session_state.kick_start).total_seconds() // 60)
        st.markdown(
            f"<div style='text-align:center; font-size:2.2rem; font-weight:900; color:#ff6b6b;'>"
            f"{st.session_state.kick_count}"
            f"<span style='font-size:1rem; color:#888;'> / 10회</span></div>",
            unsafe_allow_html=True,
        )
        st.progress(min(st.session_state.kick_count / 10, 1.0))
        if st.session_state.kick_count >= 10:
            st.success("✅ 정상! 2시간 내 10회 달성")
        elif elapsed_min >= 120:
            st.warning("⚠️ 2시간 경과, 10회 미만이면 병원에 연락하세요")
        st.caption(f"측정 시작: {st.session_state.kick_start.strftime('%H:%M')} · 경과 {elapsed_min}분")
        ck1, ck2 = st.columns(2)
        with ck1:
            if st.button("👶 태동!", key="kick_btn"):
                st.session_state.kick_count += 1
                st.rerun()
        with ck2:
            if st.button("초기화", key="kick_reset"):
                st.session_state.kick_count = 0
                st.session_state.kick_start = now
                st.rerun()

    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    st.link_button("📊 태교 편지 보러가기", REAL_SHEET_URL)
    st.divider()
    st.markdown("<div style='text-align:center; color:#ff6b6b; font-weight:800; font-size:0.9rem;'>📞 마더세이프 1588-7309</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#888; font-size:0.78rem; margin-top:4px;'>임신·수유 중 약물 안전 상담</div>", unsafe_allow_html=True)

# ==========================================
# 메인 타이틀
# ==========================================
st.markdown("<h2 style='text-align:center; color:#ff6b6b; margin-bottom:6px;'>💖 이레 안심 가이드</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; margin-bottom:24px;'>임신 초기부터 육아까지 — 이레 엄마·아빠를 위한 백과사전</p>", unsafe_allow_html=True)

# ==========================================
# 탭 구성 (8개)
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📅 주차별 가이드",
    "🥗 음식 안전",
    "💊 약물 안전",
    "🏥 검사·기록",
    "👶 육아 백과",
    "💬 AI 상담",
    "🚨 응급·진통",
    "👨‍👩‍👧 휴가·휴직",
    "📋 준비 도구",
])

STATUS_ICON = {"ok": "⭕", "warn": "⚠️", "no": "❌"}
STATUS_CLASS = {"ok": "food-ok", "warn": "food-warn", "no": "food-no"}
STATUS_COLOR = {"ok": "#27ae60", "warn": "#e67e22", "no": "#e74c3c"}

# ──────────────────────────────────────────
# TAB 1: 주차별 가이드
# ──────────────────────────────────────────
with tab1:
    clamped = min(max(current_weeks, 1), 40)
    data = WEEK_DATA[clamped]
    st.markdown(f"""
    <div class="week-hero">
        <h1>👶 {current_weeks}주 {current_days_rem}일차</h1>
        <p>태아 크기: <b>{data['size']}</b> &nbsp;|&nbsp; 출산 예정일까지 <b>{"D-Day!" if d_day <= 0 else f"D-{d_day}"}</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 원하는 주차 직접 보기")
    selected_week = st.slider("임신 주차 선택", 1, 40, clamped, format="%d주")
    sel = WEEK_DATA[selected_week]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">👶 {selected_week}주차 이레 상태</div>
            <b>크기:</b> {sel['size']}<br><br>
            {sel['fetal']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card card-blue">
            <div class="card-title card-title-blue">🤱 엄마 몸의 변화</div>
            {sel['mom']}
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card card-green">
            <div class="card-title card-title-green">🙋‍♂️ 이레 아빠 미션</div>
            {sel['dad']}<br><br>
            <i style="color:#888;">이레 엄마, 오늘도 고생 많았어요. 사랑해요! 💕</i>
        </div>
        """, unsafe_allow_html=True)

        # ✅ 아빠 미션 체크 (NEW)
        mission_key = f"dad_mission_done_w{selected_week}"
        done = st.checkbox(f"✅ {selected_week}주차 아빠 미션 완료!", key=mission_key)
        if done and not st.session_state.get(mission_key + "_saved"):
            save_to_sheets("아빠미션", f"{selected_week}주차 미션 완료: {sel['dad']}")
            st.session_state[mission_key + "_saved"] = True
            st.toast("아빠 미션 완료 기록! 💪")
        done_weeks = sorted([int(k.replace("dad_mission_done_w", "")) for k, v in st.session_state.items()
                             if k.startswith("dad_mission_done_w") and not k.endswith("_saved") and v])
        if done_weeks:
            st.caption(f"이번 세션 완료한 미션: {', '.join(str(w)+'주' for w in done_weeks)}")

        st.markdown(f"""
        <div class="card card-orange">
            <div class="card-title card-title-orange">⚠️ 이번 주 주의사항</div>
            {sel['caution']}
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 📋 임신 전 기간 한눈에 보기")
    trimester = st.radio("분기 선택", ["1분기 (1~13주)", "2분기 (14~27주)", "3분기 (28~40주)"], horizontal=True)
    t_map = {"1분기 (1~13주)": range(1, 14), "2분기 (14~27주)": range(14, 28), "3분기 (28~40주)": range(28, 41)}
    week_range = t_map[trimester]

    for w in week_range:
        d = WEEK_DATA[w]
        is_current = (w == current_weeks)
        current_label = " 👈 현재" if is_current else ""
        with st.expander(f"**{w}주차** — {d['size']}{current_label}"):
            cc1, cc2 = st.columns(2)
            with cc1:
                st.markdown(f"**👶 태아:** {d['fetal']}")
                st.markdown(f"**🤱 엄마:** {d['mom']}")
            with cc2:
                st.markdown(f"**🙋‍♂️ 아빠:** {d['dad']}")
                st.markdown(f"**⚠️ 주의:** {d['caution']}")

# ──────────────────────────────────────────
# TAB 2: 음식 안전 가이드
# ──────────────────────────────────────────
with tab2:
    st.markdown("### 🥗 임신 중 음식 안전 가이드")
    st.markdown("""
    <div class="card card-green" style="margin-bottom:16px;">
        <div class="card-title card-title-green">범례</div>
        <span class="food-ok">⭕ 안전 (추천)</span>&nbsp;&nbsp;
        <span class="food-warn">⚠️ 주의 (소량·조건부)</span>&nbsp;&nbsp;
        <span class="food-no">❌ 금지</span><br>
        <span style="color:#888; font-size:0.82rem;">※ 생선 수은 관련 기준은 식약처 '임신·수유 여성 생선 안전 섭취 가이드'를 참고했으며, 세부 권장량은 최신 자료로 확인하세요.</span>
    </div>
    """, unsafe_allow_html=True)

    search_food = st.text_input("🔍 음식 검색", placeholder="예: 커피, 고등어, 달걀...")

    for category, items in FOOD_GUIDE.items():
        filtered = [i for i in items if not search_food or search_food.lower() in i["name"].lower() or search_food in i["name"]]
        if not filtered:
            continue
        st.markdown(f"#### {category}")
        for item in filtered:
            icon = STATUS_ICON[item["status"]]
            cls = STATUS_CLASS[item["status"]]
            st.markdown(f"""
            <div style="background:#fff; border-radius:12px; padding:14px 18px; margin-bottom:10px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.05); border-left:4px solid {STATUS_COLOR[item['status']]};">
                <span class="{cls}" style="font-size:1.1rem;">{icon} {item['name']}</span><br>
                <span style="color:#666; font-size:0.88rem; margin-top:4px; display:block;">{item['reason']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div class="card card-purple">
        <div class="card-title card-title-purple">💊 임신 중 영양제 가이드</div>
        <b>필수:</b> 엽산 400~800㎍ (임신 전~12주), 철분 30mg (16주 이후), 칼슘 1000mg<br>
        <b>권장:</b> 오메가3 (DHA 200mg 이상), 비타민D 600~2000IU<br>
        <b>주의:</b> 비타민A 과다 (선천성 기형 위험), 종합비타민 선택 시 성분 확인 필수<br>
        <b>복용 시기:</b> 엽산은 임신 전부터, 철분은 식후 복용 (흡수 개선)<br>
        <span style="color:#888; font-size:0.82rem;">※ 개인 상태(빈혈·당뇨 등)에 따라 달라지므로 주치의와 상의하세요.</span>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────
# TAB 3: 💊 약물 안전 가이드 (NEW)
# ──────────────────────────────────────────
with tab3:
    st.markdown("### 💊 임신 중 약물 안전 가이드")
    st.markdown("""
    <div class="card card-red" style="margin-bottom:16px;">
        <div class="card-title card-title-red">⚠️ 반드시 읽어주세요</div>
        아래 정보는 <b>일반적으로 알려진 참고 정보</b>이며, 임신 주차·개인 상태·제품 성분에 따라 판단이 달라집니다.<br>
        <b>모든 약은 복용 전 산부인과 전문의 또는 약사와 상담</b>하고,
        궁금한 약이 있으면 <b>마더세이프 상담센터 ☎ 1588-7309</b> (한국마더세이프전문상담센터)에 무료로 문의하세요.<br>
        <span style="color:#e74c3c; font-weight:700;">이미 복용한 약이 걱정된다면 자책하지 말고 먼저 마더세이프에 전화하세요 — 대부분 괜찮은 경우가 많습니다.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-green" style="margin-bottom:16px;">
        <div class="card-title card-title-green">범례</div>
        <span class="food-ok">⭕ 비교적 안전하다고 알려짐 (상담 후 사용)</span>&nbsp;&nbsp;
        <span class="food-warn">⚠️ 조건부·시기별 주의 (반드시 상담)</span>&nbsp;&nbsp;
        <span class="food-no">❌ 금기 또는 사용 제한 권고</span>
    </div>
    """, unsafe_allow_html=True)

    search_drug = st.text_input("🔍 약물 검색", placeholder="예: 타이레놀, 감기약, 제산제...")

    for category, items in DRUG_GUIDE.items():
        filtered = [i for i in items if not search_drug or search_drug.lower() in i["name"].lower() or search_drug in i["name"]]
        if not filtered:
            continue
        st.markdown(f"#### {category}")
        for item in filtered:
            icon = STATUS_ICON[item["status"]]
            cls = STATUS_CLASS[item["status"]]
            st.markdown(f"""
            <div style="background:#fff; border-radius:12px; padding:14px 18px; margin-bottom:10px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.05); border-left:4px solid {STATUS_COLOR[item['status']]};">
                <span class="{cls}" style="font-size:1.1rem;">{icon} {item['name']}</span><br>
                <span style="color:#666; font-size:0.88rem; margin-top:4px; display:block;">{item['reason']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div class="card card-blue">
        <div class="card-title card-title-blue">💡 약국·병원에서 이렇게 말하세요</div>
        1. "현재 <b>임신 ○○주차</b>입니다"라고 먼저 알리기<br>
        2. 복용 중인 영양제·다른 약을 함께 말하기<br>
        3. 처방받은 약 이름을 사진으로 남겨두기 (AI 상담 탭에서 사진으로 물어볼 수도 있어요)<br>
        4. 애매하면 마더세이프 ☎ 1588-7309
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────
# TAB 4: 검사 일정 + 검진 결과 기록장 + 주치의 질문 노트
# ──────────────────────────────────────────
with tab4:
    st.markdown("### 🏥 산전·산후 검사 일정표")

    st.markdown("""
    <div class="card card-blue" style="margin-bottom:20px;">
        <div class="card-title card-title-blue">검사 유형 안내</div>
        <span class="badge badge-red">필수</span> 반드시 받아야 하는 검사 &nbsp;
        <span class="badge badge-blue">선택</span> 권고 또는 선택 사항 &nbsp;
        <span class="badge badge-orange">고위험군</span> 고위험 산모 해당 &nbsp;
        <span class="badge badge-gray">자가 체크</span> 집에서 확인
    </div>
    """, unsafe_allow_html=True)

    TYPE_BADGE = {
        "필수": "badge-red",
        "선택": "badge-blue",
        "고위험군": "badge-orange",
        "GCT 이상 시": "badge-orange",
        "권고": "badge-blue",
        "필요시": "badge-gray",
        "증상시": "badge-gray",
        "자가 체크": "badge-gray",
    }

    for period_data in EXAM_SCHEDULE:
        # 🔧 버그 수정: 범위를 숫자로 파싱해 현재 주차 포함 여부 판단
        nums = re.findall(r"\d+", period_data["period"])
        lo, hi = int(nums[0]), int(nums[-1])
        is_now = lo <= current_weeks <= hi
        label = f"📌 {period_data['period']}" + (" 👈 지금" if is_now else "")
        with st.expander(label, expanded=is_now):
            for exam in period_data["exams"]:
                badge_cls = TYPE_BADGE.get(exam["type"], "badge-gray")
                st.markdown(f"""
                <div style="background:#fff; border-radius:12px; padding:14px 18px; margin-bottom:10px;
                            box-shadow:0 2px 8px rgba(0,0,0,0.04); border-left:4px solid #5b8dee;">
                    <b style="font-size:1rem;">{exam['name']}</b>
                    <span class="badge {badge_cls}" style="margin-left:8px;">{exam['type']}</span><br>
                    <span style="color:#666; font-size:0.88rem;">{exam['desc']}</span>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # 📝 주치의 질문 노트 (NEW)
    st.markdown("### 📝 주치의 질문 노트")
    st.caption("진료실에 들어가면 꼭 까먹는 질문들 — 미리 적어두고 검진 때 열어보세요. (시트에도 함께 저장됩니다)")
    if "doc_questions" not in st.session_state:
        st.session_state.doc_questions = []
    new_q = st.text_input("다음 검진 때 물어볼 것", key="doc_q_input", placeholder="예: 철분제 복용 후 속이 불편한데 바꿔도 되나요?")
    qc1, qc2 = st.columns([1, 1])
    with qc1:
        if st.button("➕ 질문 추가", key="doc_q_add"):
            if new_q.strip():
                st.session_state.doc_questions.append({"q": new_q.strip(), "time": now.strftime("%m/%d %H:%M")})
                save_to_sheets("주치의질문", new_q.strip())
                st.rerun()
    with qc2:
        if st.session_state.doc_questions and st.button("🗑️ 목록 비우기", key="doc_q_clear"):
            st.session_state.doc_questions = []
            st.rerun()
    for i, q in enumerate(st.session_state.doc_questions, 1):
        st.markdown(f"""
        <div style="background:#fff; border-radius:12px; padding:12px 16px; margin-bottom:8px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.04); border-left:4px solid #a29bfe;">
            <b>Q{i}.</b> {q['q']} <span style="color:#aaa; font-size:0.78rem;">({q['time']})</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 📈 검진 결과 기록장 (NEW)
    st.markdown("### 📈 검진 결과 기록장")
    st.caption("검진일마다 태아 예상 체중(EFW)과 의사 코멘트를 기록하세요. 시트에 함께 저장되며, 그래프는 이번 세션 입력분 기준입니다.")
    if "checkup_records" not in st.session_state:
        st.session_state.checkup_records = []
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        rec_week = st.number_input("검진 시 주차", min_value=4, max_value=42, value=int(min(max(current_weeks, 4), 42)), key="rec_week")
    with rc2:
        rec_efw = st.number_input("태아 예상 체중 (g)", min_value=0, max_value=6000, value=0, step=10, key="rec_efw")
    with rc3:
        rec_bp = st.text_input("엄마 혈압 (선택)", key="rec_bp", placeholder="예: 110/70")
    rec_note = st.text_input("의사 코멘트·메모", key="rec_note", placeholder="예: 성장 정상, 다음 검진 2주 뒤")
    if st.button("💾 검진 기록 저장", key="rec_save"):
        record = {"week": int(rec_week), "efw": int(rec_efw), "bp": rec_bp, "note": rec_note, "date": now.strftime("%Y-%m-%d")}
        st.session_state.checkup_records.append(record)
        save_to_sheets("검진기록", json.dumps(record, ensure_ascii=False))
        st.toast("검진 기록 저장 완료! 📈")
        st.rerun()

    if st.session_state.checkup_records:
        recs = sorted(st.session_state.checkup_records, key=lambda r: r["week"])
        efw_rows = {f"{r['week']}주": r["efw"] for r in recs if r["efw"] > 0}
        if len(efw_rows) >= 2:
            st.markdown("**태아 체중 추이 (g)**")
            st.line_chart(efw_rows)
        st.markdown("**기록 목록**")
        for r in recs[::-1]:
            bp_str = f" · 혈압 {r['bp']}" if r["bp"] else ""
            efw_str = f" · EFW {r['efw']}g" if r["efw"] > 0 else ""
            st.markdown(f"""
            <div style="background:#fff; border-radius:12px; padding:12px 16px; margin-bottom:8px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.04); border-left:4px solid #00cec9;">
                <b>{r['week']}주차</b> ({r['date']}){efw_str}{bp_str}<br>
                <span style="color:#666; font-size:0.88rem;">{r['note']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🍼 신생아 예방접종 일정")
    st.caption("※ 표준 예방접종 일정은 변경될 수 있으니 질병관리청 '예방접종도우미(nip.kdca.go.kr)'에서 최신 일정을 확인하세요.")
    for v in VACCINATION:
        badges = "".join([f'<span class="badge badge-purple">{vax}</span>' for vax in v["vaccines"]])
        st.markdown(f"""
        <div style="display:flex; align-items:flex-start; padding:12px 0; border-bottom:1px solid #f0e8ea;">
            <div style="min-width:110px; font-weight:800; color:#6c5ce7;">{v['age']}</div>
            <div>{badges}</div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────
# TAB 5: 육아 백과 + 육아 로그
# ──────────────────────────────────────────
with tab5:
    st.markdown("### 👶 월령별 육아 백과 (0~24개월)")
    if baby_mode:
        st.success("🎉 이레가 태어났네요! 아래 '육아 로그'로 수유·기저귀·수면을 기록해 보세요.")

    # 🍼 육아 로그 (NEW) — 출산 후 자동 강조
    with st.expander("🍼 육아 로그 (수유·기저귀·수면 기록)", expanded=baby_mode):
        st.caption("버튼 한 번으로 기록! 시트에도 함께 저장됩니다. (화면 목록은 이번 세션 기준)")
        if "baby_log" not in st.session_state:
            st.session_state.baby_log = []

        def add_baby_log(kind):
            entry = {"kind": kind, "time": datetime.now(KST)}
            st.session_state.baby_log.append(entry)
            save_to_sheets("육아로그", kind, entry["time"].strftime("%Y-%m-%d %H:%M"))

        bl1, bl2, bl3, bl4 = st.columns(4)
        with bl1:
            if st.button("🍼 수유", key="log_feed"):
                add_baby_log("수유")
                st.rerun()
        with bl2:
            if st.button("💩 기저귀", key="log_diaper"):
                add_baby_log("기저귀")
                st.rerun()
        with bl3:
            if st.button("😴 잠들었어요", key="log_sleep"):
                add_baby_log("수면시작")
                st.rerun()
        with bl4:
            if st.button("🌞 깼어요", key="log_wake"):
                add_baby_log("기상")
                st.rerun()

        last_feed = next((e for e in reversed(st.session_state.baby_log) if e["kind"] == "수유"), None)
        if last_feed:
            mins = int((datetime.now(KST) - last_feed["time"]).total_seconds() // 60)
            st.markdown(f"<div style='text-align:center; font-size:1.1rem;'>마지막 수유: <b style='color:#ff6b6b;'>{mins}분 전</b> ({last_feed['time'].strftime('%H:%M')})</div>", unsafe_allow_html=True)

        if st.session_state.baby_log:
            today_log = [e for e in st.session_state.baby_log if e["time"].date() == today_date]
            feed_n = sum(1 for e in today_log if e["kind"] == "수유")
            diaper_n = sum(1 for e in today_log if e["kind"] == "기저귀")
            st.caption(f"오늘: 수유 {feed_n}회 · 기저귀 {diaper_n}회")
            st.markdown("**최근 기록**")
            for e in st.session_state.baby_log[-8:][::-1]:
                st.markdown(f"- {e['time'].strftime('%H:%M')} — {e['kind']}")
            if st.button("🗑️ 로그 초기화", key="log_clear"):
                st.session_state.baby_log = []
                st.rerun()

    st.markdown("<p style='color:#888;'>이레가 태어난 후 월령별 발달·수유·수면·주의사항을 한눈에 확인하세요.</p>", unsafe_allow_html=True)

    for baby in BABY_CARE:
        with st.expander(f"🌱 {baby['range']}"):
            b1, b2 = st.columns(2)
            with b1:
                st.markdown(f"""
                <div class="card {baby['color']}">
                    <div class="card-title {baby['title_color']}">🧠 발달 상황</div>
                    {baby['development']}
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="card card-green">
                    <div class="card-title card-title-green">🍼 수유 & 이유식</div>
                    {baby['feeding']}
                </div>
                """, unsafe_allow_html=True)

            with b2:
                st.markdown(f"""
                <div class="card card-blue">
                    <div class="card-title card-title-blue">😴 수면 패턴</div>
                    {baby['sleep']}
                </div>
                """, unsafe_allow_html=True)

                milestones_html = "".join([f'<span class="badge badge-purple">✔ {m}</span> ' for m in baby["milestones"]])
                st.markdown(f"""
                <div class="card card-purple">
                    <div class="card-title card-title-purple">🏆 이달의 발달 이정표</div>
                    {milestones_html}
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card card-orange">
                <div class="card-title card-title-orange">🛁 돌봄 포인트</div>
                {baby['care']}
            </div>
            <div class="card card-red">
                <div class="card-title card-title-red">⚠️ 주의사항</div>
                {baby['caution']}
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div class="card card-teal">
        <div class="card-title card-title-teal">🚨 즉시 병원이 필요한 신생아 응급 상황</div>
        <b style="color:#e74c3c;">다음 증상은 즉시 응급실로!</b><br><br>
        • 38도 이상 고열 (생후 3개월 미만)<br>
        • 수유 거부가 8시간 이상 지속<br>
        • 지속적인 구토 또는 설사 (탈수 위험)<br>
        • 숨소리가 빠르거나 가슴이 움푹 들어감<br>
        • 입술·손발톱이 파랗게 변함<br>
        • 경련·발작<br>
        • 황달이 눈 흰자까지 번짐 (생후 2주 이후)
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────
# TAB 6: AI 상담 (사진 업로드 + 대화 저장 + 초기화 버그 수정)
# ──────────────────────────────────────────
with tab6:
    st.markdown("### 💬 AI 상담 — 이레 아빠 전용 챗봇")
    st.markdown(f"""
    <div class="card card-blue" style="margin-bottom:16px;">
        <div class="card-title card-title-blue">📌 이용 안내</div>
        현재 <b>{current_weeks}주차</b> 이레 맞춤으로 답변드려요.<br>
        증상·음식·약물·태교·육아 무엇이든 물어보세요! <b>📷 사진(약 포장·음식 등)도 올릴 수 있어요.</b><br>
        <span style="color:#e74c3c; font-size:0.85rem;">※ AI 답변은 참고용이며, 이상 증상은 반드시 전문의와 상담하세요. 약물은 마더세이프 1588-7309.</span>
    </div>
    """, unsafe_allow_html=True)

    # 🔧 개선: 클라이언트 초기화 실패 시 탭이 죽지 않도록
    client = None
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except Exception:
        st.warning("⚠️ OpenAI API 키가 설정되지 않아 AI 상담을 사용할 수 없어요. (.streamlit/secrets.toml에 OPENAI_API_KEY 설정)")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"안녕 이레 엄마! 현재 {current_weeks}주차네요 😊 증상, 먹거리, 약물, 태교, 육아 뭐든 편하게 물어봐요! 사진으로도 물어볼 수 있어요 📷"}
        ]

    # 📷 사진 업로드 (NEW)
    uploaded_img = st.file_uploader("📷 사진으로 질문하기 (약 포장, 음식, 성분표 등)", type=["png", "jpg", "jpeg"], key="chat_img")
    if uploaded_img:
        st.image(uploaded_img, width=200, caption="질문과 함께 이 사진을 보낼게요")

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    prompt = st.chat_input("증상, 음식, 약물, 태교, 육아 등 무엇이든 물어보세요...")

    if prompt and client is None:
        st.error("API 키 설정 후 이용해 주세요.")
    elif prompt:
        # 화면·기록용 텍스트 (사진 첨부 여부 표시)
        display_prompt = prompt + (" 📷(사진 첨부)" if uploaded_img else "")
        st.session_state.messages.append({"role": "user", "content": display_prompt})
        with st.chat_message("user"):
            st.markdown(display_prompt)
        with st.chat_message("assistant"):
            sys_msg = {
                "role": "system",
                "content": (
                    f"너는 산부인과·소아과 관련 지식을 갖춘 따뜻하고 다정한 AI 가이드야. "
                    f"지금 이레 엄마는 임신 {current_weeks}주차이고, 출산 예정일은 {due_date.strftime('%Y년 %m월 %d일')}이야. "
                    f"임신·육아·태교·음식·약물 관련 질문에 근거 있게 답하되, 확실하지 않은 것은 확실하지 않다고 말해. "
                    f"먹거리 질문엔 ⭕(안전) ❌(금지) ⚠️(주의)로 명확히 표시해줘. "
                    f"약물 질문엔 반드시 전문의·약사 상담과 마더세이프(1588-7309)를 안내하고, 사진 속 약이라도 최종 판단은 전문가에게 맡기라고 해줘. "
                    f"응급이 의심되는 증상(출혈, 파수, 태동 감소, 심한 두통 등)엔 즉시 병원 방문을 최우선으로 안내해줘. "
                    f"답변 끝에 항상 이레 엄마를 응원하는 한마디를 덧붙여줘. "
                    f"답변은 한국어로, 마크다운 형식으로 가독성 좋게 작성해줘."
                )
            }
            # 히스토리(텍스트) + 현재 메시지(사진 있으면 vision 형식)
            api_messages = [sys_msg] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]
            ]
            if uploaded_img:
                img_b64 = base64.b64encode(uploaded_img.getvalue()).decode("utf-8")
                mime = "image/png" if uploaded_img.name.lower().endswith(".png") else "image/jpeg"
                api_messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_b64}"}},
                    ],
                })
            else:
                api_messages.append({"role": "user", "content": prompt})

            try:
                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=api_messages,
                    stream=True,
                )
                full_msg = st.write_stream(res)
            except Exception as e:
                full_msg = f"⚠️ 답변 생성 중 오류가 발생했어요: {e}"
                st.error(full_msg)
        st.session_state.messages.append({"role": "assistant", "content": full_msg})

    # 🔧 버그 수정: 초기화·저장 버튼을 chat_input 블록 밖으로 이동
    bc1, bc2 = st.columns(2)
    with bc1:
        if st.button("🔄 대화 초기화", key="chat_reset"):
            st.session_state.messages = [
                {"role": "assistant", "content": f"새로운 대화를 시작해요! 현재 {current_weeks}주차 이레 엄마, 무엇이든 물어보세요 🥰"}
            ]
            st.rerun()
    with bc2:
        if st.button("💾 대화 시트에 저장", key="chat_save"):
            convo_text = "\n".join([f"[{m['role']}] {m['content']}" for m in st.session_state.messages])
            if save_to_sheets("AI상담기록", convo_text[:4000]):
                st.toast("대화 저장 완료! 📊")
            else:
                st.error("저장 실패 — 네트워크를 확인해 주세요.")

# ──────────────────────────────────────────
# TAB 7: 🚨 응급·진통 (행동 플로우 + 배뭉침 타이머)
# ──────────────────────────────────────────
with tab7:
    st.markdown("### 🚨 상황별 응급 행동 가이드")
    st.markdown("""
    <div class="card card-red" style="margin-bottom:16px;">
        <div class="card-title card-title-red">먼저 아래 연락처를 채워두세요</div>
        급할 때 찾지 않도록, 지금 미리 입력해 두세요. (이 화면에 표시용 — 앱을 껐다 켜면 다시 입력해야 해요)
    </div>
    """, unsafe_allow_html=True)
    ec1, ec2 = st.columns(2)
    with ec1:
        hosp_name = st.text_input("🏥 출산 병원 이름", key="hosp_name", placeholder="예: ○○여성병원 분만실")
    with ec2:
        hosp_tel = st.text_input("📞 병원 전화번호", key="hosp_tel", placeholder="예: 02-1234-5678")
    if hosp_name or hosp_tel:
        st.markdown(f"""
        <div style="background:#fff0f0; border:2px solid #e74c3c; border-radius:14px; padding:16px; text-align:center; margin-bottom:16px;">
            <span style="font-size:1.1rem; font-weight:800; color:#e74c3c;">🏥 {hosp_name if hosp_name else '병원'}</span><br>
            <span style="font-size:1.5rem; font-weight:900;">{hosp_tel if hosp_tel else '전화번호를 입력하세요'}</span><br>
            <span style="color:#888; font-size:0.82rem;">응급 시: 119 · 약물 상담: 마더세이프 1588-7309</span>
        </div>
        """, unsafe_allow_html=True)

    for flow in EMERGENCY_FLOW:
        with st.expander(f"{flow['title']} — {flow['urgency']}"):
            for i, step in enumerate(flow["steps"], 1):
                st.markdown(f'<div class="flow-step"><span class="flow-num">{i}</span>{step}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-orange" style="margin-top:8px;">
        <div class="card-title card-title-orange">가진통 vs 진진통 구분</div>
        <b>가진통(브랙스턴-힉스):</b> 불규칙, 강도 일정, 자세를 바꾸거나 쉬면 사라짐<br>
        <b>진진통:</b> 규칙적, 점점 강해지고 간격이 짧아짐, 쉬어도 계속됨 → 아래 타이머로 확인!
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ⏱️ 배뭉침 타이머 (기존 기능 이동)
    st.markdown("### ⏱️ 배뭉침(진통) 타이머")
    st.caption("💡 경과 시간은 버튼을 누를 때마다 갱신돼요. 진행 중 화면을 갱신하려면 '⏱️ 현재 시간 갱신'을 누르세요.")

    if "contractions" not in st.session_state:
        st.session_state.contractions = []
    if "contraction_start" not in st.session_state:
        st.session_state.contraction_start = None

    ct1, ct2 = st.columns(2)
    with ct1:
        if st.session_state.contraction_start is None:
            if st.button("▶️ 배뭉침 시작", use_container_width=True, key="con_start"):
                st.session_state.contraction_start = datetime.now(KST)
                st.rerun()
        else:
            elapsed_sec = int((datetime.now(KST) - st.session_state.contraction_start).total_seconds())
            st.markdown(
                f"<div style='background:#fff3cd; border-radius:12px; padding:14px; text-align:center;'>"
                f"⏱️ <b>진행 중</b><br>"
                f"<span style='font-size:1.6rem; font-weight:900; color:#e67e22;'>{elapsed_sec}초</span><br>"
                f"<span style='font-size:0.8rem; color:#888;'>시작: {st.session_state.contraction_start.strftime('%H:%M:%S')}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button("⏱️ 현재 시간 갱신", key="con_refresh"):
                st.rerun()
    with ct2:
        if st.session_state.contraction_start is not None:
            if st.button("⏹️ 배뭉침 종료", use_container_width=True, key="con_end"):
                end_time = datetime.now(KST)
                duration_sec = int((end_time - st.session_state.contraction_start).total_seconds())
                interval_min = None
                if st.session_state.contractions:
                    last_end = st.session_state.contractions[-1]["end"]
                    interval_min = round((st.session_state.contraction_start - last_end).total_seconds() / 60, 1)
                st.session_state.contractions.append({
                    "no": len(st.session_state.contractions) + 1,
                    "start": st.session_state.contraction_start,
                    "end": end_time,
                    "duration_sec": duration_sec,
                    "interval_min": interval_min,
                })
                st.session_state.contraction_start = None
                st.rerun()
        if st.session_state.contractions:
            if st.button("🗑️ 기록 초기화", use_container_width=True, key="con_clear"):
                st.session_state.contractions = []
                st.session_state.contraction_start = None
                st.rerun()

    if st.session_state.contractions:
        recent = st.session_state.contractions[-5:][::-1]
        st.markdown("**최근 기록**")
        rows_html = ""
        for c in recent:
            interval_str = f"{c['interval_min']}분" if c['interval_min'] is not None else "—"
            rows_html += (
                f"<tr><td style='padding:8px 12px; text-align:center;'>{c['no']}번</td>"
                f"<td style='padding:8px 12px; text-align:center;'>{c['duration_sec']}초</td>"
                f"<td style='padding:8px 12px; text-align:center; "
                f"{'color:#e74c3c; font-weight:700;' if c['interval_min'] is not None and c['interval_min'] <= 10 else ''}'>"
                f"{interval_str}</td>"
                f"<td style='padding:8px 12px; color:#888;'>{c['start'].strftime('%H:%M')}</td></tr>"
            )
        st.markdown(
            f"<table style='width:100%; border-collapse:collapse; background:#fff; border-radius:12px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.05);'>"
            f"<thead><tr style='background:#fdf0f0;'>"
            f"<th style='padding:10px 12px;'>회차</th><th style='padding:10px 12px;'>지속시간</th>"
            f"<th style='padding:10px 12px;'>간격</th><th style='padding:10px 12px;'>시작시간</th>"
            f"</tr></thead><tbody>{rows_html}</tbody></table>",
            unsafe_allow_html=True,
        )
        intervals = [c["interval_min"] for c in st.session_state.contractions if c["interval_min"] is not None]
        if intervals and min(intervals[-3:]) <= 10:
            st.error("🚨 간격 10분 이하! 규칙적이면 즉시 병원으로 출발하세요.")
        elif intervals and min(intervals[-3:]) <= 15:
            st.warning("⚠️ 간격이 좁아지고 있어요. 계속 관찰하세요.")

# ──────────────────────────────────────────
# TAB 8: 👨‍👩‍👧 휴가·휴직 (제도 요약 + 계산기) (NEW)
# ──────────────────────────────────────────
with tab8:
    st.markdown("### 👨‍👩‍👧 출산휴가·육아휴직 한눈에 보기")
    st.markdown("""
    <div class="card card-orange" style="margin-bottom:16px;">
        <div class="card-title card-title-orange">⚠️ 기준 안내 (2026-07 기준)</div>
        아래 내용과 계산 결과는 <b>2026년 시행 기준(고용노동부 고시·고용보험법령)</b>을 반영한 <b>참고용 추정치</b>입니다.
        상한액·제도는 매년 바뀌고, 통상임금 산정은 회사마다 다르므로
        <b>정확한 금액은 고용24(work24.go.kr) 모의계산과 회사 인사팀 확인</b>이 우선입니다.
        회사 취업규칙에 법정 기준보다 유리한 규정이 있을 수도 있어요.
    </div>
    """, unsafe_allow_html=True)

    # ── 제도 요약 카드 ──────────────────────
    for lv in LEAVE_SUMMARY:
        with st.expander(f"{lv['name']} — {lv['period']}"):
            st.markdown(f"""
            <div class="card card-blue" style="margin-bottom:0;">
                <b>대상:</b> {lv['who']}<br>
                <b>기간:</b> {lv['period']}<br>
                <b>핵심 포인트:</b> {lv['point']}<br>
                <b>급여:</b> {lv['pay']}<br>
                <b>신청:</b> {lv['apply']}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── 계산기 1: 출산전후휴가 날짜·급여 ──────
    st.markdown("#### 🗓️ 출산전후휴가 계산기 (엄마)")
    m1, m2, m3 = st.columns(3)
    with m1:
        mat_due = st.date_input("출산(예정)일", due_date, key="mat_due")
    with m2:
        mat_type = st.selectbox("구분", ["단태아", "다태아"], key="mat_type")
    with m3:
        mat_wage = st.number_input("월 통상임금 (원)", min_value=0, value=3_000_000, step=100_000, key="mat_wage")
    mat_company = st.radio("회사 규모", ["우선지원대상기업 (중소기업 등)", "대규모 기업"], horizontal=True, key="mat_comp")

    rule = LEAVE_RULES["출산전후휴가"]
    total_d = rule["총일수"][mat_type]
    post_min = rule["출산후최소"][mat_type]
    paid_d = rule["유급일수"][mat_type]
    cap_total = rule["급여상한_총액"][mat_type]
    pre_max = total_d - post_min  # 출산 전 최대 사용 가능일
    earliest_start = mat_due - timedelta(days=pre_max - 1)
    latest_end = mat_due + timedelta(days=post_min)

    monthly_cap = 2_200_000  # 2026년 월(30일) 기준 상한
    eb_monthly = min(mat_wage, monthly_cap)  # 고용보험 월 지급 추정
    if mat_company.startswith("우선지원"):
        eb_total = round(cap_total * min(mat_wage / monthly_cap, 1.0)) if mat_wage < monthly_cap else cap_total
        employer_extra = max(0, (mat_wage - monthly_cap)) * (paid_d // 30)  # 유급구간 상한 초과분 사업주 부담
        pay_desc = f"고용보험에서 전체 {total_d}일 지원 (총 상한 {cap_total:,}원)"
    else:
        eb_total = eb_monthly * ((total_d - paid_d) // 30)  # 마지막 무급구간만 고용보험
        employer_extra = mat_wage * (paid_d // 30)          # 최초 유급구간은 사업주 통상임금 100%
        pay_desc = f"최초 {paid_d}일 사업주 유급 + 마지막 {total_d - paid_d}일 고용보험 (월 상한 {monthly_cap:,}원)"

    st.markdown(f"""
    <div class="card card-green" style="margin-top:8px;">
        <div class="card-title card-title-green">계산 결과</div>
        <b>총 휴가일수:</b> {total_d}일 (역일 기준) · 출산 후 <b>{post_min}일 이상</b> 반드시 확보<br>
        <b>가장 빠른 시작 가능일:</b> {earliest_start.strftime('%Y.%m.%d')} (출산 전 최대 {pre_max}일)<br>
        <b>휴가 종료(예상):</b> {latest_end.strftime('%Y.%m.%d')} 전후<br>
        <b>급여 구조:</b> {pay_desc}<br>
        <b>고용보험 수령 추정:</b> 약 {eb_total:,}원
        {f"+ 사업주 유급분 약 {employer_extra:,}원" if employer_extra > 0 else ""}<br>
        <span style="color:#888; font-size:0.82rem;">※ 출산이 예정일보다 늦어져 출산 후 {post_min}일이 부족해지면 휴가는 연장되지만 연장분은 무급일 수 있어요.
        미숙아 출산 시 100일로 확대(2026년 총 상한 7,333,330원). 정확한 금액은 고용24 모의계산 필수.</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── 계산기 2: 배우자 출산휴가 ─────────────
    st.markdown("#### 👨 배우자 출산휴가 계산기 (아빠)")
    p1, p2 = st.columns(2)
    with p1:
        pat_birth = st.date_input("아기 출생일 (예정일)", due_date, key="pat_birth")
    with p2:
        pat_wage = st.number_input("아빠 월 통상임금 (원)", min_value=0, value=3_500_000, step=100_000, key="pat_wage")
    pat_company = st.radio("회사 규모", ["우선지원대상기업 (중소기업 등)", "대규모 기업"], horizontal=True, key="pat_comp")

    p_rule = LEAVE_RULES["배우자출산휴가"]
    pat_deadline = pat_birth + timedelta(days=p_rule["사용기한_일"])
    # 통상임금 20일분 추정: 월 통상임금 ÷ 209시간 × 8시간 × 20일 (주 40시간 기준 근사치)
    pat_daily = pat_wage / 209 * 8
    pat_20d = round(pat_daily * p_rule["일수"])
    pat_cap = p_rule["급여상한_20일"]
    if pat_company.startswith("우선지원"):
        pat_eb = min(pat_20d, pat_cap)
        pat_employer = max(0, pat_20d - pat_cap)
        pat_desc = f"고용보험이 20일 전체 지원 (상한 {pat_cap:,}원) — 초과분은 사업주 부담"
    else:
        pat_eb = 0
        pat_employer = pat_20d
        pat_desc = "대규모 기업은 사업주가 20일 전체 유급 부담 (고용보험 지원 없음)"

    st.markdown(f"""
    <div class="card card-green" style="margin-top:8px;">
        <div class="card-title card-title-green">계산 결과</div>
        <b>휴가일수:</b> 20일 (근무일 기준 — 주말·공휴일 제외, 연속 사용 시 실제 약 4주)<br>
        <b>사용 기한:</b> 출생일부터 120일 이내 → <b>{pat_deadline.strftime('%Y.%m.%d')}까지</b><br>
        <b>분할:</b> 3회까지 분할 가능 (총 4개 구간)<br>
        <b>급여 구조:</b> {pat_desc}<br>
        <b>20일분 통상임금 추정:</b> 약 {pat_20d:,}원
        (고용보험 약 {pat_eb:,}원{f" + 사업주 약 {pat_employer:,}원" if pat_employer > 0 else ""})<br>
        <span style="color:#888; font-size:0.82rem;">※ 20일분 통상임금은 주 40시간(월 209시간) 기준 근사 계산입니다.
        실제는 회사 급여 규정에 따라 다르니 인사팀에 확인하세요. 휴가 미부여 시 사업주 과태료 500만원.</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── 계산기 3: 육아휴직 급여 ───────────────
    st.markdown("#### 👶 육아휴직 급여 계산기 (엄마·아빠 각각)")
    g1, g2, g3 = st.columns(3)
    with g1:
        pl_wage = st.number_input("월 통상임금 (원)", min_value=0, value=3_000_000, step=100_000, key="pl_wage")
    with g2:
        pl_months = st.number_input("휴직 개월 수", min_value=1, max_value=18, value=12, key="pl_months")
    with g3:
        pl_66 = st.checkbox("6+6 부모육아휴직제 적용", key="pl_66",
                            help="생후 18개월 내 부모 모두 육아휴직 사용 시 첫 6개월 상한 인상 (각자 적용)")

    pl_rule = LEAVE_RULES["육아휴직"]
    monthly_pays = []
    for m in range(1, int(pl_months) + 1):
        if pl_66 and m <= 6:
            rate, cap = 1.00, pl_rule["육육상한"][m - 1]
        else:
            for limit, r, c in pl_rule["급여구간"]:
                if m <= limit:
                    rate, cap = r, c
                    break
        pay = min(pl_wage * rate, cap)
        pay = max(pay, pl_rule["하한"]) if pl_wage > 0 else 0
        monthly_pays.append(round(pay))
    pl_total = sum(monthly_pays)

    seg_html = ""
    seg_ranges = [(1, 3), (4, 6), (7, 12), (13, 18)]
    for s, e in seg_ranges:
        seg = [monthly_pays[i - 1] for i in range(s, min(e, int(pl_months)) + 1) if i <= int(pl_months)]
        if seg:
            if len(set(seg)) == 1:
                seg_html += f"<b>{s}~{min(e, int(pl_months))}개월:</b> 월 {seg[0]:,}원<br>"
            else:
                seg_html += f"<b>{s}~{min(e, int(pl_months))}개월:</b> 월 {min(seg):,}~{max(seg):,}원<br>"

    over12_warn = ""
    if pl_months > 12:
        over12_warn = "<span style='color:#e67e22; font-weight:700;'>⚠️ 13개월 이후는 부모 모두 각 3개월 이상 사용 / 한부모 / 중증장애아동 부모 조건 충족 시에만 가능해요.</span><br>"

    st.markdown(f"""
    <div class="card card-green" style="margin-top:8px;">
        <div class="card-title card-title-green">계산 결과 (1인 기준)</div>
        {seg_html}
        <b>총 수령 추정액 ({int(pl_months)}개월):</b>
        <span style="font-size:1.3rem; font-weight:900; color:#ff6b6b;">약 {pl_total:,}원</span><br>
        {over12_warn}
        <span style="color:#888; font-size:0.82rem;">※ 하한 월 70만원 적용. 사후지급금은 폐지되어 전액 휴직 중 지급됩니다.
        6+6은 부모 각자에게 적용되므로 두 분 모두 계산해 합산해 보세요.
        구간별 상한은 변경될 수 있으니 최종 확인은 고용24 모의계산으로.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-purple">
        <div class="card-title card-title-purple">📌 신청 절차 요약 (육아휴직)</div>
        1️⃣ <b>휴직 시작 30일 전</b>까지 회사에 육아휴직 신청서 제출<br>
        2️⃣ 회사가 고용24에 <b>육아휴직 확인서</b> 등록<br>
        3️⃣ 휴직 시작 1개월 후부터 본인이 <b>고용24에서 급여 신청</b> (매월 또는 일괄 — 종료 후 12개월 이내)<br>
        4️⃣ 조건: 고용보험 피보험 단위기간 180일 이상 · 만 8세(초2) 이하 자녀 (임신 중 사용 가능)
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────
# TAB 9: 📋 준비 도구
# (체중 트래커 · 준비물 체크리스트 · 정부 지원 · 마음 체크 · 홈 화면 추가)
# ──────────────────────────────────────────
with tab9:
    st.markdown("### 📋 임신·출산 준비 도구")

    # ── 1. 체중 트래커 (BMI 연동 개선) ──────
    st.markdown("#### ⚖️ 체중 트래커")
    wt1, wt2, wt3 = st.columns(3)
    with wt1:
        pre_weight = st.number_input("임신 전 체중 (kg)", min_value=30.0, max_value=150.0, value=55.0, step=0.1, key="wt_pre")
    with wt2:
        height_cm = st.number_input("키 (cm)", min_value=140.0, max_value=200.0, value=163.0, step=0.1, key="wt_ht")
    with wt3:
        cur_weight = st.number_input("현재 체중 (kg)", min_value=30.0, max_value=150.0, value=pre_weight, step=0.1, key="wt_cur")

    gain = round(cur_weight - pre_weight, 1)
    bmi = pre_weight / ((height_cm / 100) ** 2)

    # 미국의학한림원(IOM 2009) 권고 기준 — 임신 전 BMI별 총 증가 권장 범위
    if bmi < 18.5:
        bmi_label, rec_min, rec_max = "저체중", 12.5, 18.0
    elif bmi < 25.0:
        bmi_label, rec_min, rec_max = "정상", 11.5, 16.0
    elif bmi < 30.0:
        bmi_label, rec_min, rec_max = "과체중", 7.0, 11.5
    else:
        bmi_label, rec_min, rec_max = "비만", 5.0, 9.0

    # 🔧 개선: 주차별 예상 범위를 BMI별 총 권장량과 연동
    # 1분기(~13주) 총 0.5~2kg 가정, 이후 잔여분을 40주까지 선형 배분
    FIRST_TRI_MIN, FIRST_TRI_MAX = 0.5, 2.0
    if current_weeks <= 13:
        exp_min = round(FIRST_TRI_MIN * (current_weeks / 13), 1)
        exp_max = round(FIRST_TRI_MAX * (current_weeks / 13), 1)
    else:
        frac = min((current_weeks - 13) / 27, 1.0)
        exp_min = round(FIRST_TRI_MIN + (rec_min - FIRST_TRI_MIN) * frac, 1)
        exp_max = round(FIRST_TRI_MAX + (rec_max - FIRST_TRI_MAX) * frac, 1)

    if gain < exp_min:
        wt_status = ("🔵 체중 증가가 적어요", "#2c7be5", "단백질·철분 섭취를 늘려보세요. 지속되면 주치의와 상의하세요.")
    elif gain <= exp_max:
        wt_status = ("✅ 적정 범위예요!", "#27ae60", "잘 유지하고 계세요. 균형 잡힌 식단을 유지하세요.")
    else:
        wt_status = ("🟠 증가량이 많아요", "#e67e22", "고칼로리·고나트륨 음식을 줄이고 가벼운 산책을 해보세요. 급격한 증가는 주치의 상담.")

    st.markdown(f"""
    <div class="card card-blue" style="margin-top:12px;">
        <div class="card-title card-title-blue">분석 결과</div>
        <b>임신 전 BMI:</b> {bmi:.1f} ({bmi_label})<br>
        <b>총 체중 증가량:</b> <span style="font-size:1.3rem; font-weight:900; color:#ff6b6b;">{'+' if gain >= 0 else ''}{gain}kg</span><br>
        <b>{current_weeks}주차 예상 증가 범위 (BMI 연동):</b> +{exp_min}~{exp_max}kg<br>
        <b>임신 전체 권장 증가량:</b> {rec_min}~{rec_max}kg<br><br>
        <span style="color:{wt_status[1]}; font-weight:700;">{wt_status[0]}</span><br>
        <span style="color:#666; font-size:0.9rem;">{wt_status[2]}</span><br>
        <span style="color:#aaa; font-size:0.78rem;">※ 권장 범위는 일반 기준(IOM 2009)이며 다태아·개인 상태에 따라 다릅니다. 주치의 안내가 우선입니다.</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💾 오늘 체중 시트에 기록", key="wt_save"):
        if save_to_sheets("체중기록", f"{current_weeks}주차 {cur_weight}kg (증가 {gain}kg)"):
            st.toast("체중 기록 저장 완료! ⚖️")

    st.divider()

    # ── 2. 출산 준비물 체크리스트 (버그 수정) ─────────
    st.markdown("#### 🎒 출산 준비물 체크리스트")

    total_items = sum(len(v) for v in CHECKLIST.values())
    checked_count = sum(
        1 for category, items in CHECKLIST.items()
        for item in items
        if st.session_state.get(f"chk_{category}_{item}", False)
    )
    progress_val = checked_count / total_items if total_items > 0 else 0

    st.markdown(f"**전체 진행률: {checked_count} / {total_items}개 완료**")
    st.progress(progress_val)
    if progress_val == 1.0:
        st.success("🎉 모든 준비가 완료됐어요! 이레 곧 만나요!")

    for category, items in CHECKLIST.items():
        cat_checked = sum(1 for item in items if st.session_state.get(f"chk_{category}_{item}", False))
        with st.expander(f"{category} ({cat_checked}/{len(items)})"):
            for item in items:
                st.checkbox(item, key=f"chk_{category}_{item}")

    cl1, cl2 = st.columns(2)
    with cl1:
        if st.button("✅ 전체 완료 표시", use_container_width=True):
            # 🔧 버그 수정: 위젯 key를 직접 변경해야 화면에 반영됨
            for category, items in CHECKLIST.items():
                for item in items:
                    st.session_state[f"chk_{category}_{item}"] = True
            st.rerun()
    with cl2:
        if st.button("🔄 전체 초기화", use_container_width=True):
            for category, items in CHECKLIST.items():
                for item in items:
                    st.session_state[f"chk_{category}_{item}"] = False
            st.rerun()

    st.divider()

    # ── 3. 🏛️ 정부 지원·행정 절차 (NEW) ─────
    st.markdown("#### 🏛️ 정부 지원금·행정 절차 체크")
    st.markdown("""
    <div class="card card-orange" style="margin-bottom:12px;">
        <div class="card-title card-title-orange">⚠️ 확인 안내</div>
        지원 <b>금액·소득 기준·신청 방법은 매년 바뀝니다.</b> 아래는 항목·시기 안내이며,
        최신 기준은 <b>복지로(bokjiro.go.kr)</b>와 <b>정부24(gov.kr)</b>, 거주지 행정복지센터에서 꼭 확인하세요.
    </div>
    """, unsafe_allow_html=True)
    for g in GOV_SUPPORT:
        gk = f"gov_{g['name']}"
        col_g1, col_g2 = st.columns([0.08, 0.92])
        with col_g1:
            st.checkbox("", key=gk, label_visibility="collapsed")
        with col_g2:
            done_style = "opacity:0.55;" if st.session_state.get(gk) else ""
            st.markdown(f"""
            <div style="background:#fff; border-radius:12px; padding:12px 16px; margin-bottom:8px; {done_style}
                        box-shadow:0 2px 8px rgba(0,0,0,0.04); border-left:4px solid #fd9644;">
                <b>{g['name']}</b> <span class="badge badge-orange">{g['when']}</span><br>
                <span style="color:#666; font-size:0.88rem;">신청: {g['how']}<br>💡 {g['note']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── 4. 💗 엄마 마음 체크 (NEW) ───────────
    st.markdown("#### 💗 엄마 마음 체크")
    st.markdown("""
    <div class="card card-purple" style="margin-bottom:12px;">
        <div class="card-title card-title-purple">이건 진단이 아니에요</div>
        임신·출산 전후엔 호르몬 변화로 기분이 크게 출렁이는 게 자연스러워요.
        아래는 <b>스스로 돌아보는 참고용 체크</b>일 뿐, 어떤 진단도 아닙니다.<br>
        다만 <b>가라앉는 기분이 2주 이상 대부분의 날 지속</b>되거나 일상이 힘들어지면,
        산부인과 주치의나 정신건강 전문가와 꼭 이야기해 보세요. 도움을 받는 건 강한 선택이에요.
    </div>
    """, unsafe_allow_html=True)
    mc1 = st.select_slider("요즘 웃거나 즐거운 일이", options=["예전처럼 있어요", "조금 줄었어요", "많이 줄었어요"], key="mind1")
    mc2 = st.select_slider("잠은 (아기 때문이 아닌데도)", options=["잘 자요", "가끔 설쳐요", "자주 설쳐요"], key="mind2")
    mc3 = st.select_slider("이유 없이 불안하거나 눈물이 나는 날이", options=["거의 없어요", "가끔 있어요", "자주 있어요"], key="mind3")
    mind_free = st.text_area("지금 마음을 한 줄로 적어볼까요? (선택)", key="mind_free", placeholder="쓰는 것만으로도 정리가 돼요")

    heavy = sum(1 for v in [mc1, mc2, mc3] if v in ("많이 줄었어요", "자주 설쳐요", "자주 있어요"))
    if heavy >= 2:
        st.markdown("""
        <div class="card card-red">
            <div class="card-title card-title-red">요즘 많이 힘드신 것 같아요</div>
            혼자 견디지 않아도 돼요. 남편에게 이 화면을 보여주는 것부터 시작해도 좋아요.<br><br>
            📞 <b>보건복지상담센터 129</b> (연중무휴)<br>
            📞 <b>정신건강 위기상담 1577-0199</b><br>
            🏥 다음 산부인과 검진 때 주치의에게 기분 변화를 꼭 말씀해 주세요.
        </div>
        """, unsafe_allow_html=True)
    elif heavy == 1:
        st.info("조금 지쳐 있는 날들이 있는 것 같아요. 산책·수다·충분한 휴식으로 스스로를 돌봐주시고, 계속되면 주치의와 이야기해 보세요.")
    else:
        st.success("마음 컨디션이 안정적인 편이네요. 지금처럼 자주 스스로를 돌봐주세요 💗")

    if st.button("💾 마음 기록 저장", key="mind_save"):
        content = f"웃음:{mc1} / 수면:{mc2} / 불안:{mc3} / 메모:{mind_free}"
        if save_to_sheets("마음체크", content):
            st.toast("마음 기록 저장 완료 💗")

    st.divider()

    # ── 5. 📱 홈 화면에 앱처럼 추가하기 (NEW) ─
    with st.expander("📱 이 앱을 휴대폰 홈 화면에 추가하기"):
        st.markdown("""
**아이폰 (Safari)**
1. Safari로 이 앱 주소를 열어요
2. 하단 **공유 버튼(⬆️)** 탭
3. **'홈 화면에 추가'** 선택 → 이름을 '이레 가이드'로 → 추가

**안드로이드 (Chrome)**
1. Chrome으로 이 앱 주소를 열어요
2. 우측 상단 **⋮ 메뉴** 탭
3. **'홈 화면에 추가'** 선택

**⏰ 알림이 필요하다면 (검진일·영양제 등)**
Streamlit 앱은 자체 푸시 알림이 없어요. 아이폰 **미리 알림** 또는 **캘린더**에
검진 예약일·영양제 시간을 등록해서 함께 쓰는 걸 추천해요.
        """)

    st.markdown("""
    <div style="text-align:center; color:#bbb; font-size:0.75rem; margin-top:24px;">
        이 앱의 의학 정보는 참고용이며 진단·처방을 대신하지 않습니다.<br>
        이상 증상 시 산부인과·소아과 전문의와 상담하세요. · 약물 상담: 마더세이프 1588-7309
    </div>
    """, unsafe_allow_html=True)
