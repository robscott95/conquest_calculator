# unit_stats.py
import streamlit as st
import json

from common_util import show_special_abilities_block
from target_unit.summary_block import show as show_summary_block
def show():
    st.header("Target unit:")

    # Collapsible section for Unit Stats
    with st.expander("Unit Stats", expanded=True):
        defense = st.slider('Defense', min_value=0, max_value=6, value=2)
        evasion = st.slider('Evasion', min_value=0, max_value=6, value=1)
        resolve = st.slider('Resolve', min_value=0, max_value=6, value=3)
        stands = st.slider('Stands', min_value=0, max_value=20, value=3)

    # Collapsible section for Special Abilities
    with st.expander("Special Abilities", expanded=True):
        show_special_abilities_block("target")
    
    # # Calculation and display area outside of collapsible context, responsive to input changes
    show_summary_block(defense, evasion, resolve, stands)
    # show_roll_stats_block(no_of_attacks, no_of_stands_all, no_of_stands_engaged)