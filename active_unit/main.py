# unit_stats.py
import streamlit as st
import json

from util import calc_expected_hits, generate_pill_label
from active_unit.summary_block import show as show_summary_block
from active_unit.roll_stats_block import show as show_roll_stats_block
from active_unit.special_abilities_block import show as show_special_abilities_block


# Load and initialize session state for storing values and tracking modifications if not already present
if 'special_abilities_values' not in st.session_state:
    with open('active_unit/special_abilities.json', 'r') as f:
        st.session_state.special_abilities_values = json.load(f)
        for ability in st.session_state.special_abilities_values.keys():
            st.session_state.special_abilities_values[ability]["is_modified"] = False

def show():
    st.header("Active unit's stat block:")

    # Collapsible section for Unit Stats
    with st.expander("Unit Stats", expanded=True):
        target = st.slider('Target value (Clash / Volley)', min_value=1, max_value=6, value=3)
        no_of_attacks = st.slider('No of die (Attacks / Barrage)', min_value=1, max_value=20, value=4)
        no_of_stands_all = st.slider('No of Stands', min_value=1, max_value=20, value=3)
        no_of_stands_engaged = st.slider('No of Engaged Stands', min_value=0, max_value=no_of_stands_all, value=min(no_of_stands_all, 4))

    # Collapsible section for Special Abilities
    with st.expander("Special Abilities", expanded=True):
        show_special_abilities_block()
    
    # Calculation and display area outside of collapsible context, responsive to input changes
    show_summary_block(target, no_of_attacks, no_of_stands_engaged, no_of_stands_all)
    show_roll_stats_block(no_of_attacks, no_of_stands_all, no_of_stands_engaged)