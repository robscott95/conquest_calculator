import streamlit as st

def show():
    action_type = st.radio("Action:", ["Clash", "Volley", "Charge", "Charge + Clash"])
    is_flank_attack = st.checkbox("Flank/Rear attack")

    return {
        "action_type": action_type,
        "is_flank_attack": is_flank_attack
    }