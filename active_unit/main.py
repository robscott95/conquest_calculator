# unit_stats.py
import streamlit as st
import json

from active_unit.summary_block import show as show_summary_block
from active_unit.roll_stats_block import show as show_roll_stats_block
from common_util import show_special_abilities_block

def show():
    st.header("Active unit:")

    # Collapsible section for Unit Stats
    with st.expander("Unit Stats", expanded=True):
        if 'target_attack' not in st.session_state:
            st.session_state.target_attack = 3
        if 'no_of_attacks' not in st.session_state:
            st.session_state.no_of_attacks = 4
        if 'no_of_stands_all' not in st.session_state:
            st.session_state.no_of_stands_all = 3
        if 'no_of_stands_engaged' not in st.session_state:
            st.session_state.no_of_stands_engaged = 3

        st.session_state.target_attack = st.slider('Target value', min_value=1, max_value=6, value=st.session_state.target_attack)
        st.session_state.no_of_attacks = st.slider('Number of attacks', min_value=1, max_value=20, value=st.session_state.no_of_attacks)
        st.session_state.no_of_stands_all = st.slider('Stands', min_value=1, max_value=20, value=st.session_state.no_of_stands_all)
        st.session_state.no_of_stands_engaged = st.slider('Attacking Stands', min_value=0, max_value=st.session_state.no_of_stands_all, value=st.session_state.no_of_stands_engaged)
    # Collapsible section for Special Abilities
    with st.expander("Special Abilities", expanded=True):
        show_special_abilities_block("active")
    st.session_state.action_type = st.radio("Action:", ["Clash", "Volley"])
    
    # Calculation and display area outside of collapsible context, responsive to input changes
    show_summary_block(st.session_state.target_attack, st.session_state.no_of_attacks, st.session_state.no_of_stands_engaged, st.session_state.no_of_stands_all)