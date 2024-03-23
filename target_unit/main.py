# unit_stats.py
import streamlit as st
import json

from common_util import show_special_abilities_block
from target_unit.summary_block import show as show_summary_block
from target_unit.roll_stats_block import show as show_roll_stats_block

def show():
    st.header("Target unit's stats:")

    # Collapsible section for Unit Stats
    with st.expander("Unit Stats", expanded=True):
        defense = st.slider('Defense', min_value=0, max_value=6, value=2)
        evasion = st.slider('Evasion', min_value=0, max_value=6, value=1)
        resolve = st.slider('Resolve', min_value=0, max_value=6, value=3)

    # Collapsible section for Special Abilities
    with st.expander("Special Abilities", expanded=True):
        show_special_abilities_block("target")
    
    # # Calculation and display area outside of collapsible context, responsive to input changes
    # show_summary_block(target, no_of_attacks, no_of_stands_engaged, no_of_stands_all)
    # show_roll_stats_block(no_of_attacks, no_of_stands_all, no_of_stands_engaged)