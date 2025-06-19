import streamlit as st
import time
import os

# Set up page
st.set_page_config(page_title="LoL Jungle Timer", layout="wide")
st.title("🕒 LoL Jungle Timer")

# Define camps for each side, with optional image paths
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

# Initialize session state
for key in ("timers", "confirm", "confirm_time"):
    if key not in st.session_state:
        st.session_state[key] = {}

# Auto-clear confirm prompts after 3 seconds
for camp, ts in list(st.session_state["confirm_time"].items()):
    if time.time() - ts > 3:
        st.session_state["confirm"].pop(camp, None)
        st.session_state["confirm_time"].pop(camp, None)

def handle_press(camp, duration):
    """Start timer, or toggle/cancel based on confirm state."""
    timers = st.session_state["timers"]
    confirm = st.session_state["confirm"]
    ctime = st.session_state["confirm_time"]

    if camp not in timers:
        # Start timer
        timers[camp] = time.time() + duration
        confirm.pop(camp, None)
        ctime.pop(camp, None)
    else:
        # Already running: either ask to cancel or actually cancel
        if not confirm.get(camp, False):
            confirm[camp] = True
            ctime[camp] = time.time()
        else:
            timers.pop(camp, None)
            confirm.pop(camp, None)
            ctime.pop(camp, None)

# Display camps in pairs
for (camp_left, data_left), (camp_right, data_right) in zip(left_camps.items(), right_camps.items()):
    col1, col2 = st.columns(2)

    # Left side
    with col1:
        if os.path.exists(data_left["img"]):
            st.image(data_left["img"], width=80)
        else:
            st.markdown(f"**{camp_left}**")
        end = st.session_state["timers"].get(camp_left, 0)
        rem = int(end - time.time()) if end else -1
        status = "READY" if rem <= 0 else f"{rem//60}:{rem%60:02d}"
        st.markdown(f"{status}")
        btn = "Start" if camp_left not in st.session_state["timers"] else (
              "Cancel?" if st.session_state["confirm"].get(camp_left, False) else "Start")
        if st.button(btn, key=f"L_{camp_left}"):
            handle_press(camp_left, data_left["time"])

    # Right side
    with col2:
        if os.path.exists(data_right["img"]):
            st.image(data_right["img"], width=80)
        else:
            st.markdown(f"**{camp_right}**")
        end = st.session_state["timers"].get(camp_right, 0)
        rem = int(end - time.time()) if end else -1
        status = "READY" if rem <= 0 else f"{rem//60}:{rem%60:02d}"
        st.markdown(f"{status}")
        btn = "Start" if camp_right not in st.session_state["timers"] else (
              "Cancel?" if st.session_state["confirm"].get(camp_right, False) else "Start")
        if st.button(btn, key=f"R_{camp_right}"):
            handle_press(camp_right, data_right["time"])