import streamlit as st
import streamlit.components.v1 as components
import json
import random
import time
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

# 🥤 몬스터 음료 관련 세션 상태
if "monster_inventory" not in st.session_state:
    st.session_state.monster_inventory = 0
if "monster_bought_count" not in st.session_state:
    st.session_state.monster_bought_count = 0
if "last_reset_time" not in st.session_state:
    st.session_state.last_reset_time = datetime.now()
if "buff_end_time" not in st.session_state:
    st.session_state.buff_end_time = None

# UI 탭 세션
if "show_shop" not in st.session_state:
    st.session_state.show_shop = False
if "show_inventory" not in st.session_state:
    st.session_state.show_inventory = False
if "show_casino" not in st.session_state:
    st.session_state.show_casino = False
if "show_theme_tab" not in st.session_state:
    st.session_state.show_theme_tab = False

# 테마 세션
if "current_theme" not in st.session_state:
    st.session_state.current_theme = "다크 모드"
if "unlocked_themes" not in st.session_state:
    st.session_state.unlocked_themes = ["다크 모드"]

# ⏳ 10분 주기 횟수 리셋 체크
now = datetime.now()
if now - st.session_state.last_reset_time >= timedelta(minutes=10):
    st.session_state.monster_bought_count = 0
    st.session_state.last_reset_time = now
    st.toast("🔄 10분이 지나 몬스터 음료 구매 제한이 초기화되었습니다!")

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

# 2. 저장용 데이터 JSON 패키징
save_data_payload = json.dumps({
    "count": st.session_state.count,
    "per_click": st.session_state.per_click,
    "upgrade_count": st.session_state.upgrade_count,
    "cost": st.session_state.cost,
    "auto_clickers": st.session_state.auto_clickers,
    "auto_cost": st.session_state.auto_cost,
    "monster_inventory": st.session_state.monster_inventory,
    "monster_bought_count": st.session_state.monster_bought_count,
    "current_theme": st.session_state.current_theme,
    "unlocked_themes": st.session_state.unlocked_themes
})

# 스페이스바 키 입력 수신 스크립트
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

# 테마 적용
st.markdown(THEME_STYLES.get(st.session_state.current_theme, THEME_STYLES["다크 모드"]), unsafe_allow_html=True)
st.title("🔢 스페이스 카운터")

# 💾 사이드바: 데이터 저장/불러오기
with st.sidebar:
    st.header("💾 데이터 저장 / 불러오기")
    st.subheader("1. 내 저장 코드 복사")
    
    copy_button_html = f"""
        <button id="copyBtn" style="
            width: 100%; padding: 10px; background-color: #4CAF50; color: white;
            border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px;">
            📋 저장 코드 자동 복사하기
        </button>
        <script>
        document.getElementById('copyBtn').addEventListener('click', function() {{
            const textToCopy = {json.dumps(save_data_payload)};
            navigator.clipboard.writeText(textToCopy).then(function() {{
                alert('💾 저장 코드가 클립보드에 복사되었습니다!');
            }}).catch(function(err) {{ alert('복사 실패: ' + err); }});
        }});
        </script>
    """
    components.html(copy_button_html, height=50)
    st.code(save_data_payload, language="json")

    st.write("---")
    st.subheader("2. 저장 코드 불러오기")
    save_code_input = st.text_input("저장 코드를 붙여넣으세요", placeholder="JSON 코드를 입력하세요")
    
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
                st.session_state.monster_inventory = data.get("monster_inventory", st.session_state.monster_inventory)
                st.session_state.monster_bought_count = data.get("monster_bought_count", st.session_state.monster_bought_count)
                st.session_state.current_theme = data.get("current_theme", st.session_state.current_theme)
                st.session_state.unlocked_themes = data.get("unlocked_themes", st.session_state.unlocked_themes)
                
                st.toast("🎉 데이터 복원 성공!")
                st.rerun()
            except Exception:
                st.error("❌ 유효하지 않은 저장 코드입니다.")

# ⚡ 버프 계산 (몬스터 음료 버프 판별)
is_buff_active = False
remaining_buff_time = 0

if st.session_state.buff_end_time:
    now_ts = datetime.now()
    if now_ts < st.session_state.buff_end_time:
        is_buff_active = True
        remaining_buff_time = int((st.session_state.buff_end_time - now_ts).total_seconds())
    else:
        st.session_state.buff_end_time = None

current_per_click = st.session_state.per_click * 2 if is_buff_active else st.session_state.per_click

# 상단 버프 상태 표시
if is_buff_active:
    st.info(f"⚡ **몬스터 파워 버프 진행 중!** (클릭당 +{current_per_click} / 남은 시간: {remaining_buff_time}초)")

st.metric("현재 카운트", f"{st.session_state.count:,}")

# 클릭 동작
def increment():
    st.session_state.count += current_per_click

st.button(f"숫자 올리기 (+{current_per_click:,}) (Space 키)", on_click=increment, use_container_width=True)

st.write("---")

# 탭 메뉴
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🏪 상점", use_container_width=True):
        st.session_state.show_shop = not st.session_state.show_shop
        st.session_state.show_inventory = False
        st.session_state.show_casino = False
        st.session_state.show_theme_tab = False
with c2:
    if st.button(f"🎒 가방 ({st.session_state.monster_inventory})", use_container_width=True):
        st.session_state.show_inventory = not st.session_state.show_inventory
        st.session_state.show_shop = False
        st.session_state.show_casino = False
        st.session_state.show_theme_tab = False
with c3:
    if st.button("🎰 도박장", use_container_width=True):
        st.session_state.show_casino = not st.session_state.show_casino
        st.session_state.show_shop = False
        st.session_state.show_inventory = False
        st.session_state.show_theme_tab = False
with c4:
    if st.button("🎨 테마", use_container_width=True):
        st.session_state.show_theme_tab = not st.session_state.show_theme_tab
        st.session_state.show_shop = False
        st.session_state.show_inventory = False
        st.session_state.show_casino = False

# 🛒 상점 UI
if st.session_state.show_shop:
    with st.expander("🛒 아이템 상점", expanded=True):
        st.subheader("🥤 몬스터 에너기 (파이프라인 펀치 - 핑크)")
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            # 핑크색 몬스터 음료 이미지
            st.image("https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=300", width=120)
            
        with col_info:
            st.write("**효과**: 10초 동안 클릭당 얻는 카운트 2배")
            st.write("**가격**: 500 카운트")
            st.write(f"**구매 제한**: {st.session_state.monster_bought_count}/5 (10분마다 리셋)")
            
            if st.button(" 구매하기 (500)", use_container_width=True):
                if st.session_state.monster_bought_count >= 5:
                    st.toast("❌ 10분당 최대 5개까지만 구매할 수 있습니다.")
                elif st.session_state.count < 500:
                    st.toast("❌ 카운트가 부족합니다!")
                else:
                    st.session_state.count -= 500
                    st.session_state.monster_inventory += 1
                    st.session_state.monster_bought_count += 1
                    st.toast("🎉 몬스터 음료를 구매하여 인벤토리에 추가했습니다!")
                    st.rerun()

        st.write("---")
        st.markdown(f"**클릭 강화** (구매: {st.session_state.upgrade_count}/5)")
        if st.button(f"클릭 강화 구매 ({st.session_state.cost:,})", use_container_width=True):
            if st.session_state.count >= st.session_state.cost:
                st.session_state.count -= st.session_state.cost
                st.session_state.per_click += 1
                st.session_state.upgrade_count += 1
                st.session_state.cost = int(st.session_state.cost * 1.5)
                st.toast("🎉 클릭 강화 성공!")
                st.rerun()
            else:
                st.toast("❌ 카운트 부족")

# 🎒 인벤토리 UI
if st.session_state.show_inventory:
    with st.expander("🎒 보유 인벤토리", expanded=True):
        if st.session_state.monster_inventory > 0:
            col_inv_img, col_inv_btn = st.columns([1, 2])
            with col_inv_img:
                st.image("https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=300", width=100)
            with col_inv_btn:
                st.write(f"**몬스터 음료 (핑크)**")
                st.write(f"보유 수량: {st.session_state.monster_inventory}개")
                if st.button("🥤 마시기 (10초간 클릭수 2배)", use_container_width=True):
                    st.session_state.monster_inventory -= 1
                    st.session_state.buff_end_time = datetime.now() + timedelta(seconds=10)
                    st.toast("⚡ 몬스터 음료를 마셨습니다! 10초 동안 클릭수가 2배가 됩니다!")
                    st.rerun()
        else:
            st.info("인벤토리가 비어 있습니다. 상점에서 아이템을 구매해보세요!")

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
                st.rerun()

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
