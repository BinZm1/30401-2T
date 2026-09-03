import streamlit as st
import streamlit.components.v1 as components
import json
import random
from datetime import datetime

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

# 테마 세션
if "current_theme" not in st.session_state:
    st.session_state.current_theme = "다크 모드"
if "unlocked_themes" not in st.session_state:
    st.session_state.unlocked_themes = ["다크 모드"]

# 🎨 테마 스타일 정의
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

# 2. 현재 상태를 JSON 문자열로 패키징
save_data_payload = json.dumps({
    "count": st.session_state.count,
    "per_click": st.session_state.per_click,
    "upgrade_count": st.session_state.upgrade_count,
    "cost": st.session_state.cost,
    "auto_clickers": st.session_state.auto_clickers,
    "auto_cost": st.session_state.auto_cost,
    "current_theme": st.session_state.current_theme,
    "unlocked_themes": st.session_state.unlocked_themes
})

# 스페이스바 키 입력 수신용 스크립트
components.html(
    """
    <script>
    const parentDoc = window.parent.document;
    function handleKeyDown(e) {
        if (['INPUT', 'TEXTAREA'].includes(parentDoc.activeElement.tagName)) return;
        if (e.code === 'Space') {
            e.preventDefault();
            const btns = parentDoc.querySelectorAll('button');
            for (let btn of btns) {
                if (btn.innerText.includes('숫자 올리기')) { btn.click(); break; }
            }
        }
    }
    parentDoc.removeEventListener('keydown', handleKeyDown);
    parentDoc.addEventListener('keydown', handleKeyDown);
    </script>
    """,
    height=0,
)

# 🎨 테마 스타일 적용
st.markdown(THEME_STYLES.get(st.session_state.current_theme, THEME_STYLES["다크 모드"]), unsafe_allow_html=True)
st.title("🔢 스페이스 카운터")

# 💾 사이드바: 저장 코드 자동 복사 및 불러오기 기능
with st.sidebar:
    st.header("💾 데이터 저장 / 불러오기")
    
    st.subheader("1. 내 저장 코드 복사")
    st.caption("버튼을 누르면 저장 코드가 클립보드에 자동으로 복사됩니다.")
    
    # 📋 원클릭 자동 복사 버튼 (HTML/JS 커스텀 버튼)
    copy_button_html = f"""
        <button id="copyBtn" style="
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            font-size: 14px;">
            📋 저장 코드 자동 복사하기
        </button>
        <script>
        document.getElementById('copyBtn').addEventListener('click', function() {{
            const textToCopy = {json.dumps(save_data_payload)};
            navigator.clipboard.writeText(textToCopy).then(function() {{
                alert('💾 저장 코드가 클립보드에 복사되었습니다! 메모장이나 카카오톡 등에 붙여넣어 보관하세요.');
            }}).catch(function(err) {{
                alert('복사 실패: ' + err);
            }});
        }});
        </script>
    """
    components.html(copy_button_html, height=50)

    # 기본 코드 표시 (우측 상단 기본 복사 아이콘도 이용 가능)
    st.code(save_data_payload, language="json")

    st.write("---")
    st.subheader("2. 저장 코드 불러오기")
    save_code_input = st.text_input("복사했던 저장 코드를 붙여넣으세요", placeholder="JSON 코드를 입력하세요")
    
    if st.button("🎮 게임 데이터 불러오기", use_container_width=True):
        if save_code_input.strip():
            try:
                data = json.loads(save_code_input.strip())
                st.session_state.count = data.get("count", st.session_state.count)
                st.session_state.per_click = data.get("per_click", st.session_state.per_click)
                st.session_state.upgrade_count = data.get("upgrade_count", st.session_state.upgrade_count)
                st.session_state.cost = data.get("cost", st.session_state.cost)
                st.session_state.auto_clickers = data.get("auto_clickers", st.session_state.auto_clickers)
                st.session_state.auto_cost = data.get("auto_cost", st.session_state.auto_cost)
                st.session_state.current_theme = data.get("current_theme", st.session_state.current_theme)
                st.session_state.unlocked_themes = data.get("unlocked_themes", st.session_state.unlocked_themes)
                
                st.toast("🎉 데이터 복원 성공!")
                st.rerun()
            except Exception:
                st.error("❌ 유효하지 않은 저장 코드입니다.")

# 오토 카운터 Fragment
@st.fragment(run_every=1)
def render_auto_counter():
    st.session_state.count += st.session_state.auto_clickers
    st.metric("현재 카운트 (실시간)", f"{st.session_state.count:,}")

if st.session_state.auto_clickers > 0:
    render_auto_counter()
else:
    st.metric("현재 카운트", f"{st.session_state.count:,}")

# 클릭 동작
def increment():
    st.session_state.count += st.session_state.per_click

st.button(f"숫자 올리기 (+{st.session_state.per_click:,}) (Space 키)", on_click=increment, use_container_width=True)

st.write("---")

# 탭 메뉴
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
        selected_theme = st.radio(
            "테마 선택:", 
            options=st.session_state.unlocked_themes, 
            index=st.session_state.unlocked_themes.index(st.session_state.current_theme)
        )
        if selected_theme != st.session_state.current_theme:
            st.session_state.current_theme = selected_theme
            st.rerun()
