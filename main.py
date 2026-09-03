import streamlit as st
import streamlit.components.v1 as components
import json
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="스페이스 카운터", layout="centered")

# 1. 세션 상태 초기화
if "count" not in st.session_state:
    st.session_state.count = 0
if "per_click" not in st.session_state:
    st.session_state.per_click = 1
if "upgrade_count" not in st.session_state:
    st.session_state.upgrade_count = 0
if "cost" not in st.session_state:
    st.session_state.cost = 50
if "auto_clickers" not in st.session_state:
    st.session_state.auto_clickers = 0
if "auto_cost" not in st.session_state:
    st.session_state.auto_cost = 5000

# UI 탭 세션
if "show_shop" not in st.session_state:
    st.session_state.show_shop = False
if "show_casino" not in st.session_state:
    st.session_state.show_casino = False
if "show_theme_tab" not in st.session_state:
    st.session_state.show_theme_tab = False

if "current_theme" not in st.session_state:
    st.session_state.current_theme = "다크 모드"
if "unlocked_themes" not in st.session_state:
    st.session_state.unlocked_themes = ["다크 모드"]

if "last_save_time" not in st.session_state:
    st.session_state.last_save_time = datetime.now()

# 🎨 테마 스타일 정의 (화이트 모드 Expander 밝은 회색 적용)
THEME_STYLES = {
    "다크 모드": """
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        .stApp * { text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000 !important; }
        div[data-testid="stMetricValue"] { color: #FFFFFF !important; }
        </style>
    """,
    "화이트 모드": """
        <style>
        .stApp { background-color: #FFFFFF !important; }
        .stApp, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, 
        .stApp div, div[data-testid="stMetricValue"], .stButton>button, .stButton>button p {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            -webkit-text-stroke: 0px transparent !important;
            text-shadow: none !important;
        }
        div[data-testid="stExpander"],
        div[data-testid="stExpander"] > details,
        div[data-testid="stExpander"] summary,
        div[data-testid="stExpanderDetails"] {
            background-color: #F0F2F6 !important;
            border-color: #E0E0E0 !important;
            color: #000000 !important;
        }
        .stButton>button { 
            background-color: #FFFFFF !important; 
            color: #000000 !important;
            border: 2px solid #000000 !important; 
        }
        </style>
    """,
    "네온 시티": """
        <style>
        .stApp { background-color: #0d0221; color: #00f6ff !important; }
        .stApp * { text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 0 0 5px #00f6ff !important; }
        div[data-testid="stMetricValue"] { color: #ff007f !important; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 0 0 12px #ff007f !important; }
        .stButton>button { background-color: #241442 !important; color: #00f6ff !important; border: 1px solid #00f6ff !important; }
        </style>
    """,
    "골드 라운지": """
        <style>
        .stApp { background-color: #1a150e; color: #f3e5ab !important; }
        .stApp * { text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000 !important; }
        div[data-testid="stMetricValue"] { color: #ffd700 !important; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 0 0 10px #ffd700 !important; }
        .stButton>button { background-color: #33291a !important; color: #ffd700 !important; border: 1px solid #ffd700 !important; }
        </style>
    """,
    "레트로 픽셀": """
        <style>
        .stApp { background-color: #001100; color: #00ff00 !important; font-family: monospace; }
        .stApp * { text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 0 0 4px #00ff00 !important; }
        div[data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 0 0 8px #00ff00 !important; }
        .stButton>button { background-color: #002200 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
        </style>
    """
}

# 2. 게임 데이터를 JSON 형태 문자열로 묶기
def get_save_payload():
    return json.dumps({
        "count": st.session_state.count,
        "per_click": st.session_state.per_click,
        "upgrade_count": st.session_state.upgrade_count,
        "cost": st.session_state.cost,
        "auto_clickers": st.session_state.auto_clickers,
        "auto_cost": st.session_state.auto_cost,
        "current_theme": st.session_state.current_theme,
        "unlocked_themes": st.session_state.unlocked_themes
    })

# 3. 브라우저 저장/불러오기 자바스크립트 처리
payload_str = get_save_payload()

components.html(
    f"""
    <script>
    const parentDoc = window.parent.document;

    // 브라우저에 저장하기 함수
    function saveGameData() {{
        const payload = {json.dumps(payload_str)};
        localStorage.setItem('space_counter_save_data', payload);
        console.log("Game Data Saved:", payload);
    }}

    // 스페이스바 입력 처리
    function handleKeyDown(e) {{
        if (['INPUT', 'TEXTAREA'].includes(parentDoc.activeElement.tagName)) return;
        if (e.code === 'Space') {{
            e.preventDefault();
            const btns = parentDoc.querySelectorAll('button');
            for (let btn of btns) {{
                if (btn.innerText.includes('숫자 올리기')) {{ btn.click(); break; }}
            }}
        }}
    }}

    parentDoc.removeEventListener('keydown', handleKeyDown);
    parentDoc.addEventListener('keydown', handleKeyDown);
    </script>
    """,
    height=0,
)

# 25분 주기 자동 저장 체크
def check_auto_save():
    now = datetime.now()
    if now - st.session_state.last_save_time >= timedelta(minutes=25):
        st.session_state.last_save_time = now
        st.toast("💾 25분이 경과되어 브라우저에 자동 저장되었습니다!")

# 로드 데이터 세션 반영 함수
def load_saved_data(json_str):
    try:
        data = json.loads(json_str)
        st.session_state.count = data.get("count", 0)
        st.session_state.per_click = data.get("per_click", 1)
        st.session_state.upgrade_count = data.get("upgrade_count", 0)
        st.session_state.cost = data.get("cost", 50)
        st.session_state.auto_clickers = data.get("auto_clickers", 0)
        st.session_state.auto_cost = data.get("auto_cost", 5000)
        st.session_state.current_theme = data.get("current_theme", "다크 모드")
        st.session_state.unlocked_themes = data.get("unlocked_themes", ["다크 모드"])
        st.toast("🎮 이전 저장 데이터를 성공적으로 불러왔습니다!")
    except:
        st.toast("❌ 저장 데이터 로드 실패")

# UI 구성
st.markdown(THEME_STYLES[st.session_state.current_theme], unsafe_allow_html=True)
st.title("🔢 스페이스 카운터")

# 데이터 불러오기/저장하기 수동 영역
with st.sidebar:
    st.header("💾 데이터 관리")
    st.caption("25분마다 브라우저에 자동 저장됩니다.")
    
    # 수동 저장 기능
    if st.button("💾 지금 브라우저에 저장", use_container_width=True):
        components.html(
            f"""
            <script>
            localStorage.setItem('space_counter_save_data', {json.dumps(payload_str)});
            alert('브라우저에 저장되었습니다!');
            </script>
            """,
            height=0,
        )
        st.toast("💾 데이터가 저장되었습니다!")

    # 이전 데이터 복원용 텍스트 입력창
    st.write("---")
    save_code_input = st.text_input("복원용 저장 데이터 입력", placeholder="저장된 JSON 코드를 붙여넣으세요")
    if st.button("데이터 불러오기", use_container_width=True):
        if save_code_input.strip():
            load_saved_data(save_code_input.strip())
            st.rerun()

# 오토 카운터 Fragment
@st.fragment(run_every=1)
def render_auto_counter():
    st.session_state.count += st.session_state.auto_clickers
    check_auto_save()
    st.metric("현재 카운트 (실시간)", f"{st.session_state.count:,}")

if st.session_state.auto_clickers > 0:
    render_auto_counter()
else:
    st.metric("현재 카운트", f"{st.session_state.count:,}")

def increment():
    st.session_state.count += st.session_state.per_click
    check_auto_save()

st.button(f"숫자 올리기 (+{st.session_state.per_click:,}) (Space 키)", on_click=increment, use_container_width=True)

st.write("---")

# 탭 버튼
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏪 상점", use_container_width=True):
        st.session_state.show_shop = not st.session_state.show_shop
        st.session_state.show_casino = False
        st.session_state.show_theme_tab = False
with c2:
    if st.button("🎰 도박장", use_container_width=True):
        st.session_state.show_casino = not st.session_state.show_casino
        st.session_state.show_shop = False
        st.session_state.show_theme_tab = False
with c3:
    if st.button("🎨 테마", use_container_width=True):
        st.session_state.show_theme_tab = not st.session_state.show_theme_tab
        st.session_state.show_shop = False
        st.session_state.show_casino = False

# 🛒 상점 UI
if st.session_state.show_shop:
    with st.expander("🛒 강화 상점", expanded=True):
        st.markdown(f"**1. 클릭 강화** (구매: {st.session_state.upgrade_count}/5)")
        if st.button("클릭 강화 구매", use_container_width=True):
            if st.session_state.count >= st.session_state.cost:
                st.session_state.count -= st.session_state.cost
                st.session_state.per_click += 1
                st.session_state.upgrade_count += 1
                st.session_state.cost = int(st.session_state.cost * 1.5)
                st.toast("🎉 클릭 강화 성공!")
            else:
                st.toast("❌ 카운트 부족")

# 🎰 도박장 UI
if st.session_state.show_casino:
    with st.expander("🎰 행운의 도박장", expanded=True):
        if st.button("100 배팅", use_container_width=True):
            if st.session_state.count >= 100:
                st.session_state.count -= 100
                mult = random.choice([0.5, 2, 5])
                win = int(100 * mult)
                st.session_state.count += win
                st.toast(f"🎰 {mult}배 당첨! (+{win:,})")

# 🎨 테마 UI
if st.session_state.show_theme_tab:
    with st.expander("🎨 보유한 테마 목록", expanded=True):
        selected_theme = st.radio("테마 선택:", options=st.session_state.unlocked_themes, index=st.session_state.unlocked_themes.index(st.session_state.current_theme))
        if selected_theme != st.session_state.current_theme:
            st.session_state.current_theme = selected_theme
            st.rerun()
