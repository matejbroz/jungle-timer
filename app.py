import streamlit as st
import time
import os
from streamlit_autorefresh import st_autorefresh

# ─── 1) AUTO-REFRESH ───────────────────────────────────────────────────────────
# rerun the script every 1000 ms so our timers update live
st_autorefresh(interval=1000, limit=None, key="timer_refresh")

# ─── 2) PAGE SETUP ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="LoL Jungle Timer", layout="wide")
st.title("🕒 LoL Jungle Timer")

# ─── 3) CAMP DEFINITIONS ──────────────────────────────────────────────────────
left_camps = {
    "Blue Buff": {"time": 300, "img": "images/blue_buff.png"},
    "Gromp":     {"time": 135, "img": "images/gromp.png"},
    "Wolves":    {"time": 135, "img": "images/wolves.png"},
    "Raptors":   {"time": 135, "img": "images/raptors.png"},
    "Krugs":     {"time": 135, "img": "images/krugs.png"},
}
right_camps = {
    "Red Buff":  {"time": 300, "img": "images/red_buff.png"},
    "Krugs":     {"time": 135, "img": "images/krugs.png"},
    "Wolves":    {"time": 135, "img": "images/wolves.png"},
    "Raptors":   {"time": 135, "img": "images/raptors.png"},
    "Gromp":     {"time": 135, "img": "images/gromp.png"},
}

# ─── 4) SESSION STATE SETUP ────────────────────────────────────────────────────
for key in ("timers", "confirm", "confirm_time"):
    if key not in st.session_state:
        st.session_state[key] = {}

# Clear “Cancel?” prompts older than 3 s
for camp, ts in list(st.session_state["confirm_time"].items()):
    if time.time() - ts > 3:
        st.session_state["confirm"].pop(camp, None)
        st.session_state["confirm_time"].pop(camp, None)

# ─── 5) HANDLER ────────────────────────────────────────────────────────────────
def handle_press(camp, duration):
    timers  = st.session_state["timers"]
    confirm = st.session_state["confirm"]
    ctime   = st.session_state["confirm_time"]

    if camp not in timers:
        # start fresh
        timers[camp] = time.time() + duration
        confirm.pop(camp, None)
        ctime.pop(camp, None)
    else:
        # already running → toggle/cancel
        if not confirm.get(camp, False):
            confirm[camp] = True
            ctime[camp]  = time.time()
        else:
            timers.pop(camp, None)
            confirm.pop(camp, None)
            ctime.pop(camp, None)

# ─── 6) RENDER PAIRWISE ────────────────────────────────────────────────────────
for (campL, dataL), (campR, dataR) in zip(left_camps.items(), right_camps.items()):
    col1, col2 = st.columns(2)

    # LEFT
    with col1:
        if os.path.exists(dataL["img"]):
            st.image(dataL["img"], width=80)
        else:
            st.markdown(f"**{campL}**")
        end = st.session_state["timers"].get(campL, 0)
        rem = max(0, int(end - time.time()))
        status = "READY" if rem == 0 else f"{rem//60}:{rem%60:02d}"
        st.markdown(status)
        btn = ("Start" if campL not in st.session_state["timers"]
               else ("Cancel?" if st.session_state["confirm"].get(campL) else "Start"))
        if st.button(btn, key=f"L_{campL}"):
            handle_press(campL, dataL["time"])

    # RIGHT
    with col2:
        if os.path.exists(dataR["img"]):
            st.image(dataR["img"], width=80)
        else:
            st.markdown(f"**{campR}**")
        end = st.session_state["timers"].get(campR, 0)
        rem = max(0, int(end - time.time()))
        status = "READY" if rem == 0 else f"{rem//60}:{rem%60:02d}"
        st.markdown(status)
        btn = ("Start" if campR not in st.session_state["timers"]
               else ("Cancel?" if st.session_state["confirm"].get(campR) else "Start"))
        if st.button(btn, key=f"R_{campR}"):
            handle_press(campR, dataR["time"])