import streamlit as st
import time
import os
from streamlit_autorefresh import st_autorefresh

# ─── 1) AUTO-REFRESH ───────────────────────────────────────────────────────────
# rerun the script every 1000 ms so timers update in real time
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

# clear old confirm prompts older than 3 seconds
for key, ts in list(st.session_state["confirm_time"].items()):
    if time.time() - ts > 3:
        st.session_state["confirm"].pop(key, None)
        st.session_state["confirm_time"].pop(key, None)

# ─── 5) HANDLER ────────────────────────────────────────────────────────────────
def handle_press(identifier, duration):
    """Start timer, or toggle/cancel based on confirm state."""
    timers  = st.session_state["timers"]
    confirm = st.session_state["confirm"]
    ctime   = st.session_state["confirm_time"]

    if identifier not in timers:
        # start fresh
        timers[identifier] = time.time() + duration
        confirm.pop(identifier, None)
        ctime.pop(identifier, None)
    else:
        # already running -> ask to cancel or cancel
        if not confirm.get(identifier, False):
            confirm[identifier] = True
            ctime[identifier]  = time.time()
        else:
            timers.pop(identifier, None)
            confirm.pop(identifier, None)
            ctime.pop(identifier, None)

# ─── 6) RENDER SIDE-BY-SIDE ────────────────────────────────────────────────────
for (campL, dataL), (campR, dataR) in zip(left_camps.items(), right_camps.items()):
    col1, col2 = st.columns(2)

    # Left side
    with col1:
        identL = f"L_{campL.replace(' ', '_')}"
        # image or text fallback
        if os.path.exists(dataL['img']):
            st.image(dataL['img'], width=80)
        else:
            st.markdown(f"**{campL}**")
        # timer display
        end_ts = st.session_state['timers'].get(identL, 0)
        rem = max(0, int(end_ts - time.time()))
        status = "READY" if rem == 0 else f"{rem//60}:{rem%60:02d}"
        st.markdown(status)
        # button logic
        btn_label = (
            "Start" if identL not in st.session_state['timers']
            else ("Cancel?" if st.session_state['confirm'].get(identL) else "Start")
        )
        if st.button(btn_label, key=identL):
            handle_press(identL, dataL['time'])

    # Right side
    with col2:
        identR = f"R_{campR.replace(' ', '_')}"
        if os.path.exists(dataR['img']):
            st.image(dataR['img'], width=80)
        else:
            st.markdown(f"**{campR}**")
        end_ts = st.session_state['timers'].get(identR, 0)
        rem = max(0, int(end_ts - time.time()))
        status = "READY" if rem == 0 else f"{rem//60}:{rem%60:02d}"
        st.markdown(status)
        btn_label = (
            "Start" if identR not in st.session_state['timers']
            else ("Cancel?" if st.session_state['confirm'].get(identR) else "Start")
        )
        if st.button(btn_label, key=identR):
            handle_press(identR, dataR['time'])
