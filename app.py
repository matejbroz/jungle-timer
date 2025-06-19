import streamlit as st
import time

# Set up page
st.set_page_config(page_title="LoL Jungle Timer", layout="centered")
st.title("🕒 LoL Jungle Timer")

# Jungle camps with respawn times (seconds)
jungle_camps = {
    "Blue Buff": 300,
    "Red Buff": 300,
    "Gromp": 135,
    "Wolves": 135,
    "Raptors": 135,
    "Krugs": 135,
    "Scuttle": 150,
    "Dragon": 300,
    "Herald": 360,
    "Baron": 360
}

# Initialize session state
if "timers" not in st.session_state:
    st.session_state.timers = {}

# Display timers
for camp, respawn_time in jungle_camps.items():
    col1, col2 = st.columns([3, 1])

    with col1:
        if camp in st.session_state.timers:
            remaining = int(st.session_state.timers[camp] - time.time())
            if remaining <= 0:
                st.markdown(f"**{camp}**: READY")
            else:
                mins = remaining // 60
                secs = remaining % 60
                st.markdown(f"**{camp}**: {mins}:{secs:02d}")
        else:
            st.markdown(f"**{camp}**: READY")

    with col2:
        if st.button(f"Start", key=camp):
            st.session_state.timers[camp] = time.time() + respawn_time
