# unit_stats.py
import streamlit as st
import json

from views.special_abilities.input import show as show_input_special_abilities

def show(
    initial_defense=3,
    initial_evasion=1,
    initial_resolve=3,
    initial_target_regiment_stands=3,
    initial_wounds_per_stand=4
):
    # Collapsible section for Unit Stats
    with st.container(border=True):
        st.header("Target Unit Stats")
        defense = st.slider('Defense value', min_value=0, max_value=6, value=initial_defense)
        evasion = st.slider('Evasion value', min_value=0, max_value=6, value=initial_evasion)
        resolve = st.slider('Resolve value', min_value=0, max_value=6, value=initial_resolve)
        wounds_per_stand = st.slider('Wounds per Stand', min_value=0, max_value=30, value=initial_wounds_per_stand )
        target_regiment_stands = st.slider('Stands', min_value=0, max_value=20, value=initial_target_regiment_stands)

    # Collapsible section for Special Abilities
    with st.container(border=True):
        st.subheader("Target Unit Special Abilities",)
        special_abilities = show_input_special_abilities("target")
    # Return all relevant values
    return {
        "target_input_defense_value": defense,
        "target_input_evasion_value": evasion,
        "target_input_resolve_value": resolve,
        "target_input_stands": target_regiment_stands,
        "target_input_special_abilities": special_abilities,
        "target_input_wounds_per_stand": wounds_per_stand,
    }