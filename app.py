import streamlit as st
from active_unit.main import show as show_active_unit_input
from active_unit.summary_block import show as show_active_unit_summary
from target_unit.main import show as show_target_unit
from target_unit.summary_block import show as show_target_unit_summary
from results.main import show as show_results

import seaborn as sns
import matplotlib.pyplot as plt

import time

# Title of the app
st.title('Conquest Wound Calculator')


col1, col2, col3 = st.columns(3)


with st.sidebar:
    tab1, tab2 = st.tabs(["Active Unit", "Target Unit"])
    with tab1:
        show_active_unit_input()
    with tab2:
        show_target_unit()


with col1:
    show_active_unit_summary(st.session_state.target_attack, st.session_state.no_of_attacks, st.session_state.no_of_stands_engaged, st.session_state.no_of_stands_all)

with col2:
    show_target_unit_summary(st.session_state.defense, st.session_state.evasion, st.session_state.resolve, st.session_state.target_regiment_stands)

with col3:
    show_results()
