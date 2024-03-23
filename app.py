import streamlit as st
from active_unit.main import show as show_active_unit_input
from active_unit.summary_block import show as show_active_unit_summary
from target_unit.main import show as show_target_unit
from target_unit.summary_block import show as show_target_unit_summary
from data_model import EngagementDataModel
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

engagement_data = EngagementDataModel(
    st.session_state.target_attack,
    st.session_state.no_of_attacks,
    st.session_state.no_of_stands_all,
    st.session_state.no_of_stands_engaged,
    st.session_state.special_abilities['active'],
    st.session_state.is_leader,
    st.session_state.defense,
    st.session_state.evasion,
    st.session_state.resolve,
    st.session_state.target_regiment_stands,
    st.session_state.special_abilities['target'],
    st.session_state.is_reroll_morale,
    st.session_state.action_type
)

with col1:
    show_active_unit_summary(
        engagement_data.active_input_target_value,
        engagement_data.active_input_number_of_attacks_value,
        engagement_data.active_input_attacking_stands,
        engagement_data.active_input_supporting_stands,
        engagement_data.active_input_special_abilities
        )

with col2:
    show_target_unit_summary(
        engagement_data.target_input_defense_value,
        engagement_data.target_input_evasion_value,
        engagement_data.target_input_resolve_value,
        engagement_data.get_target_regiment_size_resolve_bonus(),
    )

with col3:
    show_results(engagement_data)
