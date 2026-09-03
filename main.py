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
    st.session_state.monster_last_reset = now_
