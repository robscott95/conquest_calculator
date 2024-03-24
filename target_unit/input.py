# unit_stats.py
import streamlit as st
import json

from special_abilities import show_special_abilities_input_block

def show(
    initial_defense=2,
    initial_evasion=1,
    initial_resolve=3,
    initial_target_regiment_stands=3
):
    st.header("Target unit:")

    # Collapsible section for Unit Stats
    with st.expander("Unit Stats", expanded=True):
        defense = st.slider('Defense', min_value=0, max_value=6, value=initial_defense)
        evasion = st.slider('Evasion', min_value=0, max_value=6, value=initial_evasion)
        resolve = st.slider('Resolve', min_value=0, max_value=6, value=initial_resolve)
        target_regiment_stands = st.slider('Stands', min_value=0, max_value=20, value=initial_target_regiment_stands)

    # Collapsible section for Special Abilities
    with st.expander("Special Abilities", expanded=True):
        # Assuming show_special_abilities_block function is adapted similarly for optional parameters
        special_abilities = show_special_abilities_input_block("target")  # Adjust this based on actual implementation

    # Return all relevant values
    return {
        "target_input_defense_value": defense,
        "target_input_evasion_value": evasion,
        "target_input_resolve_value": resolve,
        "target_input_stands": target_regiment_stands,
        "target_input_special_abilities": special_abilities  
    }