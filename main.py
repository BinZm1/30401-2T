import streamlit as st
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="스페이스 카운터 & 상점", layout="centered")

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

# 🥤 몬스터 음료 세션
if "monster_inventory" not in st.session_state:
    st.session_state.monster_inventory = 0
if "monster_bought_count" not in st.session_state:
    st.session_state.monster_bought_count = 0
if "monster_last_reset" not in st.session_state:
    st.session_state.monster_last_reset = datetime.now()
if "buff_end_time" not in st.session_state:
    st.session_state.buff_end_time = None

# 🐱 펫(고양이) & 선물 상자 세션
if "has_cat" not in st.session_state:
    st.session_state.has_cat = False
if "box_inventory" not in st.session_state:
    st.session_state.box_inventory = 0
if "last_cat_gift_time" not in st.session_state:
    st.session_state.last_cat_gift_time = datetime.now()

# UI 탭 상태
if "show_shop" not in st.session_state:
    st.session_state.show_shop = False
if "show_pet_shop" not in st.session_state:
    st.session_state.show_pet_shop = False
if "show_inventory" not in st.session_state:
    st.session_state.show_inventory = False
if "show_casino" not in st.session_state:
    st.session_state.show_casino = False
if "show_theme_tab" not in st.session_state:
    st.session_state.show_theme_tab = False
if "current_theme" not in st.session_state:
    st.session_state.current_theme = "다크 모드"
if "unlocked_themes" not in st.session_state:
    st.session_state.unlocked_themes = ["다크 모드"]

# 🎰 도박 횟수 및 쿨타임 초기화
LIMIT_CONFIG = {
    100: 10,
    1000: 5,
    10000: 50
}

if "gamble_limits" not in st.session_state:
    now = datetime.now()
    reset_time = now + timedelta(hours=1)
    st.session_state.gamble_limits = {
        100: {"remaining": 10, "reset_at": reset_time},
        1000: {"remaining": 5, "reset_at": reset_time},
        10000: {"remaining": 50, "reset_at": reset_time}
    }

# ⏳ 몬스터 음료 10분 주기 리셋
now_time = datetime.now()
if now_time - st.session_state.monster_last_reset >= timedelta(minutes=10):
    st.session_state.monster_bought_count = 0
    st.session_state.monster_last_reset = now_time

# 🐱 고양이 1분 주기 상자 획득 체크
if st.session_state.has_cat:
    if now_time - st.session_state.last_cat_gift_time >= timedelta(minutes=1):
        st.session_state.box_inventory += 1
        st.session_state.last_cat_gift_time = now_time
        st.toast("🐱 고양이 가 밖으로 뛰어가 상자를 하나 물어왔습니다! (인벤토리 확인)")

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

# 2. 쿨타임 및 리셋 체크
def check_and_reset_limits():
    now = datetime.now()
    for amount, config in st.session_state.gamble_limits.items():
        if now >= config["reset_at"]:
            config["remaining"] = LIMIT_CONFIG[amount]
            config["reset_at"] = now + timedelta(hours=1)

check_and_reset_limits()

# ⚡ 버프 계산 (몬스터 음료)
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

# 3. 로직 함수
def increment(amount=None):
    if amount is None:
        st.session_state.count += current_per_click
    else:
        st.session_state.count += amount

def toggle_tab(tab_name):
    st.session_state.show_shop = (tab_name == "shop") and not st.session_state.show_shop
    st.session_state.show_pet_shop = (tab_name == "pet_shop") and not st.session_state.show_pet_shop
    st.session_state.show_inventory = (tab_name == "inventory") and not st.session_state.show_inventory
    st.session_state.show_casino = (tab_name == "casino") and not st.session_state.show_casino
    st.session_state.show_theme_tab = (tab_name == "theme") and not st.session_state.show_theme_tab

def buy_cat():
    if st.session_state.has_cat:
        st.toast("🐱 이미 고양이를 분양받으셨습니다!")
    elif st.session_state.count >= 5000:
        st.session_state.count -= 5000
        st.session_state.has_cat = True
        st.session_state.last_cat_gift_time = datetime.now()
        st.toast("🎉 고퀄리티 픽셀 고양이를 입양했습니다! 화면 배경에서 자유롭게 노닙니다.")
    else:
        st.toast("❌ 카운트가 부족합니다! (필요: 5,000 카운트)")

def open_box():
    if st.session_state.box_inventory > 0:
        st.session_state.box_inventory -= 1
        reward = random.randint(100, 1000)
        st.session_state.count += reward
        st.toast(f"🎁 상자를 열어 +{reward:,} 카운트를 획득했습니다!", icon="🎉")
    else:
        st.toast("❌ 보유 중인 상자가 없습니다.")

def buy_monster_drink():
    if st.session_state.monster_bought_count >= 5:
        st.toast("❌ 10분당 최대 5개까지만 구매할 수 있습니다!")
    elif st.session_state.count >= 500:
        st.session_state.count -= 500
        st.session_state.monster_inventory += 1
        st.session_state.monster_bought_count += 1
        st.toast("🥤 몬스터 음료를 구매하여 인벤토리에 보관했습니다!")
    else:
        st.toast("❌ 카운트가 부족합니다! (필요: 500 카운트)")

def use_monster_drink():
    if st.session_state.monster_inventory > 0:
        st.session_state.monster_inventory -= 1
        st.session_state.buff_end_time = datetime.now() + timedelta(seconds=10)
        st.toast("⚡ 몬스터 음료 마심! 10초 동안 클릭당 카운트 2배 적용!")
    else:
        st.toast("❌ 보유 중인 몬스터 음료가 없습니다.")

def buy_upgrade():
    if st.session_state.count >= st.session_state.cost:
        st.session_state.count -= st.session_state.cost
        st.session_state.per_click += 1
        st.session_state.upgrade_count += 1
        
        multipliers = [1.25, 1.5, 2.0]
        weights = [50, 45, 5]
        chosen_multiplier = random.choices(multipliers, weights=weights, k=1)[0]
        
        new_cost = round(st.session_state.cost * chosen_multiplier)
        st.session_state.cost = int(new_cost)
        
        percent_str = f"{int((chosen_multiplier - 1) * 100)}%"
        st.toast(f"🎉 클릭 강화 성공! (가격 +{percent_str} 인상)")
    else:
        st.toast("❌ 카운트가 부족합니다!")

def buy_auto_clicker():
    if st.session_state.count >= st.session_state.auto_cost:
        st.session_state.count -= st.session_state.auto_cost
        st.session_state.auto_clickers += 1
        
        multipliers = [3, 5, 10, 15]
        weights = [10, 20, 50, 20]
        chosen_multiplier = random.choices(multipliers, weights=weights, k=1)[0]
        
        st.session_state.auto_cost *= chosen_multiplier
        st.toast(f"🤖 오토 클릭커 구매 성공! (다음 가격 {chosen_multiplier}배 상승: {st.session_state.auto_cost:,} 카운트)")
    else:
        st.toast("❌ 카운트가 부족합니다!")

def draw_theme():
    all_themes = ["다크 모드", "화이트 모드", "네온 시티", "골드 라운지", "레트로 픽셀"]
    
    if len(st.session_state.unlocked_themes) >= len(all_themes):
        st.toast("🎉 이미 모든 테마를 해금하셨습니다!")
        return

    if st.session_state.count >= 500:
        st.session_state.count -= 500
        available_themes = [t for t in all_themes if t != st.session_state.current_theme]
        chosen_theme = random.choice(available_themes)
        
        st.session_state.current_theme = chosen_theme
        if chosen_theme not in st.session_state.unlocked_themes:
            st.session_state.unlocked_themes.append(chosen_theme)
            st.toast(f"🎨 신규 테마 해금! [{chosen_theme}] (으)로 변경 및 보관함에 추가되었습니다!", icon="✨")
        else:
            st.toast(f"🎨 테마 뽑기 성공! [{chosen_theme}] (으)로 변경되었습니다!", icon="✨")
    else:
        st.toast("❌ 카운트가 부족합니다! (필요: 500 카운트)")

def gamble(amount):
    check_and_reset_limits()
    limit_info = st.session_state.gamble_limits[amount]
    
    if limit_info["remaining"] <= 0:
        st.toast("❌ 이번 시간대의 배팅 횟수를 모두 소진했습니다!")
        return
        
    if st.session_state.count >= amount:
        st.session_state.count -= amount
        limit_info["remaining"] -= 1
        
        multipliers = [0.5, 2, 5, 10]
        weights = [60, 29, 10, 1]
        
        chosen_multiplier = random.choices(multipliers, weights=weights, k=1)[0]
        winnings = int(amount * chosen_multiplier)
        
        st.session_state.count += winnings
        
        if chosen_multiplier >= 1:
            st.toast(f"🎰 대박! {chosen_multiplier}배 당첨! (+{winnings:,} 획득)", icon="🎉")
        else:
            st.toast(f"💀 꽝! {chosen_multiplier}배... ({winnings:,}만 환급)", icon="😭")
    else:
        st.toast("❌ 배팅할 카운트가 부족합니다!")

# 4. 키보드 이벤트 처리
st.components.v1.html(
    """
    <script>
    const parentDoc = window.parent.document;
    const pressedKeys = new Set();
    
    function handleKeyDown(e) {
        if (['INPUT', 'TEXTAREA'].includes(parentDoc.activeElement.tagName)) return;
        
        pressedKeys.add(e.code);
        
        if (pressedKeys.has('KeyQ') && pressedKeys.has('KeyW') && pressedKeys.has('KeyE') && pressedKeys.has('KeyR')) {
            e.preventDefault();
            const cheatBtn = parentDoc.querySelector('button[key="cheat_btn"]');
            if (cheatBtn) cheatBtn.click();
            pressedKeys.clear();
            return;
        }

        if (e.code === 'Space') {
            e.preventDefault();
            const btns = parentDoc.querySelectorAll('button');
            for (let btn of btns) {
                if (btn.innerText.includes('숫자 올리기')) {
                    btn.click();
                    break;
                }
            }
        }
    }

    function handleKeyUp(e) {
        pressedKeys.delete(e.code);
    }

    parentDoc.removeEventListener('keydown', handleKeyDown);
    parentDoc.removeEventListener('keyup', handleKeyUp);
    parentDoc.addEventListener('keydown', handleKeyDown);
    parentDoc.addEventListener('keyup', handleKeyUp);
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
    </script>
    """,
    height=0,
)

st.button("Cheat", key="cheat_btn", on_click=lambda: increment(5000), type="secondary", use_container_width=False)

# 5. UI 구성 및 테마 CSS 적용
st.markdown(THEME_STYLES[st.session_state.current_theme], unsafe_allow_html=True)

# 🐱 대형 High-Quality Pure CSS 픽셀 고양이
if st.session_state.has_cat:
    st.markdown("""
        <style>
        @keyframes floatCatHQ {
            0%   { top: 10%; left: 5%; transform: scaleX(1); }
            25%  { top: 70%; left: 75%; transform: scaleX(1); }
            50%  { top: 75%; left: 10%; transform: scaleX(-1); }
            75%  { top: 20%; left: 80%; transform: scaleX(-1); }
            100% { top: 10%; left: 5%; transform: scaleX(1); }
        }
        .hq-cat-wrapper {
            position: fixed;
            z-index: 0;
            pointer-events: none;
            opacity: 0.95;
            animation: floatCatHQ 22s ease-in-out infinite;
        }
        /* 12px 대형 픽셀 아트 고양이 */
        .hq-pixel-cat {
            width: 12px;
            height: 12px;
            background: transparent;
            box-shadow: 
                /* 귀 외곽 및 분홍 안쪽 */
                24px 0px #d35400, 72px 0px #d35400,
                24px 12px #e67e22, 36px 12px #ffa07a, 60px 12px #ffa07a, 72px 12px #e67e22,
                12px 24px #d35400, 24px 24px #e67e22, 36px 24px #e67e22, 48px 24px #d35400, 60px 24px #e67e22, 72px 24px #e67e22, 84px 24px #d35400,
                /* 머리/선글라스 */
                12px 36px #e67e22, 24px 36px #111111, 36px 36px #111111, 48px 36px #d35400, 60px 36px #111111, 72px 36px #111111, 84px 36px #e67e22,
                12px 48px #e67e22, 24px 48px #111111, 36px 48px #333333, 48px 48px #e67e22, 60px 48px #111111, 72px 48px #333333, 84px 48px #e67e22,
                /* 코 및 입, 볼, 수염 */
                0px 60px #ffffff, 12px 60px #e67e22, 24px 60px #f39c12, 36px 60px #f39c12, 48px 60px #e74c3c, 60px 60px #f39c12, 72px 60px #f39c12, 84px 60px #e67e22, 96px 60px #ffffff,
                12px 72px #d35400, 24px 72px #ffffff, 36px 72px #e67e22, 48px 72px #ffffff, 60px 72px #e67e22, 72px 72px #ffffff, 84px 72px #d35400,
                /* 몸통 및 줄무늬 */
                24px 84px #e67e22, 36px 84px #d35400, 48px 84px #e67e22, 60px 84px #d35400, 72px 84px #e67e22,
                24px 96px #e67e22, 36px 96px #ffffff, 48px 96px #ffffff, 60px 96px #ffffff, 72px 96px #e67e22, 96px 84px #d35400, 108px 72px #d35400, /* 꼬리 */
                24px 108px #e67e22, 36px 108px #f39c12, 48px 108px #f39c12, 60px 108px #f39c12, 72px 108px #e67e22, 96px 96px #e67e22, 108px 96px #ff1493, /* 꼬리 끝 */
                /* 발 (분홍 발바닥) */
                24px 120px #ff1493, 36px 120px #e67e22, 60px 120px #ff1493, 72px 120px #e67e22;
        }
        </style>
        <div class="hq-cat-wrapper">
            <div class="hq-pixel-cat"></div>
        </div>
    """, unsafe_allow_html=True)

st.title("🔢 스페이스 카운터")

st.markdown("""
    <style>
    button[key="cheat_btn"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ⚡ 버프 표시바
if is_buff_active:
    st.info(f"⚡ **몬스터 에너기 버프 활성화!** (클릭당 +{current_per_click} / 남은 시간: {remaining_buff_time}초)")

# 6. 실시간 오토 카운터 및 고양이 자동 상자 획득
@st.fragment(run_every=1)
def render_auto_counter():
    st.session_state.count += st.session_state.auto_clickers
    st.metric("현재 카운트 (실시간)", f"{st.session_state.count:,}")

if st.session_state.auto_clickers > 0 or st.session_state.has_cat:
    render_auto_counter()
else:
    st.metric("현재 카운트", f"{st.session_state.count:,}")

st.button(
    f"숫자 올리기 (+{current_per_click:,}) (Space 키)", 
    on_click=increment, 
    use_container_width=True
)

st.write("---")

# 탭 메뉴
col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
with col_btn1:
    st.button(
        f"🏪 상점 {'닫기' if st.session_state.show_shop else '열기'}", 
        on_click=lambda: toggle_tab("shop"), 
        type="primary" if st.session_state.show_shop else "secondary",
        use_container_width=True
    )
with col_btn2:
    st.button(
        f"🐾 펫 상점 {'닫기' if st.session_state.show_pet_shop else '열기'}", 
        on_click=lambda: toggle_tab("pet_shop"), 
        type="primary" if st.session_state.show_pet_shop else "secondary",
        use_container_width=True
    )
with col_btn3:
    total_inv = st.session_state.monster_inventory + st.session_state.box_inventory
    st.button(
        f"🎒 가방 ({total_inv})", 
        on_click=lambda: toggle_tab("inventory"), 
        type="primary" if st.session_state.show_inventory else "secondary",
        use_container_width=True
    )
with col_btn4:
    st.button(
        f"🎰 도박장 {'닫기' if st.session_state.show_casino else '열기'}", 
        on_click=lambda: toggle_tab("casino"), 
        type="primary" if st.session_state.show_casino else "secondary",
        use_container_width=True
    )
with col_btn5:
    st.button(
        f"🎨 테마 {'닫기' if st.session_state.show_theme_tab else '목록'}", 
        on_click=lambda: toggle_tab("theme"), 
        type="primary" if st.session_state.show_theme_tab else "secondary",
        use_container_width=True
    )

# 7. 일반 강화 & 아이템 상점 UI
if st.session_state.show_shop:
    with st.expander("🛒 강화 및 아이템 상점", expanded=True):
        st.markdown("**🥤 몬스터 음료 (핑크 - 파이프라인 펀치)**")
        col_m_img, col_m_desc = st.columns([1, 2])
        with col_m_img:
            st.image("https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=300", width=110)
        with col_m_desc:
            st.write("- **효과**: 사용 시 10초 동안 클릭당 증가량 2배")
            st.write("- **가격**: **500 카운트**")
            st.write(f"- **구매 제한**: **{st.session_state.monster_bought_count}/5** (10분마다 초기화)")
            
            can_buy_monster = (st.session_state.count >= 500) and (st.session_state.monster_bought_count < 5)
            st.button(
                "몬스터 음료 구매하기",
                key="buy_monster_btn",
                on_click=buy_monster_drink,
                disabled=not can_buy_monster,
                use_container_width=True
            )

        st.write("---")

        st.markdown(f"**1. 클릭당 증가량 +1 강화** (구매 횟수: {st.session_state.upgrade_count}/5)")
        st.write(f"- 필요 카운트: **{st.session_state.cost:,}**")
        st.write(f"- 구매 후 기본 증가 수치: **+{st.session_state.per_click + 1:,}**")
        st.caption("🎲 구매 시 가격이 랜덤 비율(+25%/+50%/+100%)로 인상됩니다.")
        
        can_buy_upgrade = st.session_state.count >= st.session_state.cost
        st.button(
            "클릭 강화 구매하기", 
            key="buy_upgrade_btn",
            on_click=buy_upgrade, 
            disabled=not can_buy_upgrade,
            use_container_width=True
        )
        
        st.write("---")
        
        st.markdown("**2. 🤖 오토 클릭커 (1초당 +1 자동 증가)**")
        if st.session_state.upgrade_count >= 5:
            st.write(f"- 필요 카운트: **{st.session_state.auto_cost:,}**")
            st.write(f"- 현재 보유량: **{st.session_state.auto_clickers}개**")
            st.caption("🎲 구매 시 다음 가격이 랜덤 배율(3배/5배/10배/15배)로 인상됩니다.")
            
            can_buy_auto = st.session_state.count >= st.session_state.auto_cost
            st.button(
                "오토 클릭커 구매하기", 
                key="buy_auto_btn",
                on_click=buy_auto_clicker, 
                disabled=not can_buy_auto,
                use_container_width=True
            )
        else:
            st.warning(f"🔒 해금 조건: 클릭 강화를 5번 구매하세요! (현재 {st.session_state.upgrade_count}/5회)")

        st.write("---")

        st.markdown(f"**3. 🎨 테마 뽑기** (현재 적용: **{st.session_state.current_theme}**)")
        st.write("- 필요 카운트: **500**")
        st.caption("🎲 현재 테마를 제외한 나머지 4개 테마 중 하나가 25% 확률로 무작위 적용되며 보관함에 저장됩니다.")
        
        can_draw_theme = st.session_state.count >= 500
        st.button(
            "🎨 테마 랜덤 뽑기 (500 카운트)", 
            key="draw_theme_btn",
            on_click=draw_theme, 
            disabled=not can_draw_theme,
            use_container_width=True
        )

# 8. 🐾 펫 상점 UI
if st.session_state.show_pet_shop:
    with st.expander("🐾 펫 상점", expanded=True):
        st.markdown("**🐱 힙스터 픽셀 고양이 (선글라스)**")
        col_pet_img, col_pet_desc = st.columns([1, 2])
        with col_pet_img:
            # 펫 상점 미리보기용 HQ 픽셀 고양이 (소형화)
            st.markdown("""
                <div style="padding: 10px 10px;">
                    <div style="width: 4px; height: 4px; background: transparent; box-shadow: 8px 0px #d35400, 24px 0px #d35400, 8px 4px #e67e22, 12px 4px #ffa07a, 20px 4px #ffa07a, 24px 4px #e67e22, 4px 8px #d35400, 8px 8px #e67e22, 16px 8px #d35400, 20px 8px #e67e22, 28px 8px #d35400, 4px 12px #e67e22, 8px 12px #111, 12px 12px #111, 20px 12px #111, 24px 12px #111, 28px 12px #e67e22, 4px 16px #e67e22, 8px 16px #f39c12, 12px 16px #e74c3c, 16px 16px #f39c12, 20px 16px #f39c12, 24px 16px #e67e22, 8px 20px #e67e22, 12px 20px #f39c12, 16px 20px #f39c12, 20px 20px #e67e22;"></div>
                </div>
            """, unsafe_allow_html=True)
        with col_pet_desc:
            st.write("- **효과**: 화면 배경에서 자유롭게 노닐며, **1분마다 밖으로 나가 선물 상자를 물어옵니다!**")
            st.write("- **상자 내용물**: 사용 시 **100 ~ 1,000 카운트** 랜덤 획득")
            st.write("- **가격**: **5,000 카운트**")
            
            if st.session_state.has_cat:
                st.success("✅ 이미 입양된 고양이입니다.")
            else:
                can_buy_pet = st.session_state.count >= 5000
                st.button(
                    "🐱 고양이 입양하기 (5,000 카운트)",
                    key="buy_cat_btn",
                    on_click=buy_cat,
                    disabled=not can_buy_pet,
                    use_container_width=True
                )

# 9. 🎒 인벤토리 UI
if st.session_state.show_inventory:
    with st.expander("🎒 내 인벤토리", expanded=True):
        has_items = False
        
        # 몬스터 음료
        if st.session_state.monster_inventory > 0:
            has_items = True
            col_inv_img, col_inv_desc = st.columns([1, 2])
            with col_inv_img:
                st.image("https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=300", width=90)
            with col_inv_desc:
                st.markdown("**🥤 몬스터 에너기 (핑크)**")
                st.write(f"보유 수량: **{st.session_state.monster_inventory}개**")
                st.caption("사용 시 10초 동안 클릭당 카운트 획득량이 2배로 늘어납니다.")
                st.button(
                    "🥤 마시기 (10초간 클릭수 2배)", 
                    key="use_monster_btn",
                    on_click=use_monster_drink,
                    use_container_width=True
                )
            st.write("---")
            
        # 고양이의 선물 상자
        if st.session_state.box_inventory > 0:
            has_items = True
            col_box_img, col_box_desc = st.columns([1, 2])
            with col_box_img:
                st.write("🎁")
            with col_box_desc:
                st.markdown("**🎁 고양이 가 물어온 상자**")
                st.write(f"보유 수량: **{st.session_state.box_inventory}개**")
                st.caption("열면 100 ~ 1,000 카운트를 무작위로 획득합니다.")
                st.button(
                    "🎁 상자 열기", 
                    key="open_box_btn",
                    on_click=open_box,
                    use_container_width=True
                )

        if not has_items:
            st.info("🎒 인벤토리가 비어 있습니다. 상점에서 아이템을 구매하거나 고양이를 입양해 보세요!")

# 10. 도박장 UI
if st.session_state.show_casino:
    with st.expander("🎰 행운의 도박장", expanded=True):
        st.markdown("**배팅 금액 및 남아있는 횟수**")
        st.caption("🎲 확률: 0.5배 (60%) | 2배 (29%) | 5배 (10%) | 10배 (1%) (1시간마다 횟수 리셋)")
        
        now = datetime.now()
        c1, c2, c3 = st.columns(3)
        
        for idx, amount in enumerate([100, 1000, 10000]):
            info = st.session_state.gamble_limits[amount]
            rem = info["remaining"]
            max_cnt = LIMIT_CONFIG[amount]
            
            time_left = info["reset_at"] - now
            minutes_left = int(time_left.total_seconds() // 60)
            
            target_col = [c1, c2, c3][idx]
            with target_col:
                st.write(f"**{amount:,} 배팅**")
                st.caption(f"남은 횟수: **{rem}/{max_cnt}**")
                if rem == 0:
                    st.caption(f"⏳ 리셋: {minutes_left}분 후")
                
                can_gamble = (st.session_state.count >= amount) and (rem > 0)
                st.button(
                    f"{amount:,} 배팅", 
                    key=f"gamble_btn_{amount}",
                    on_click=gamble, 
                    args=(amount,),
                    disabled=not can_gamble,
                    use_container_width=True
                )

# 11. 🎨 테마 보관함 탭 UI
if st.session_state.show_theme_tab:
    with st.expander("🎨 보유한 테마 목록", expanded=True):
        st.write("해금한 테마를 자유롭게 선택하여 변경할 수 있습니다.")
        
        selected_theme = st.radio(
            "적용할 테마를 선택하세요:",
            options=st.session_state.unlocked_themes,
            index=st.session_state.unlocked_themes.index(st.session_state.current_theme)
        )
        
        if selected_theme != st.session_state.current_theme:
            st.session_state.current_theme = selected_theme
            st.rerun()
