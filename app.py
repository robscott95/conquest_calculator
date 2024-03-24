import streamlit as st
from active_unit.input import show as show_active_unit_input
from active_unit.summary import show as show_active_unit_summary
from target_unit.input import show as show_target_unit
from target_unit.summary import show as show_target_unit_summary
from data_model import EngagementDataModel
from results.summary import show as show_results

import seaborn as sns
import matplotlib.pyplot as plt

import time

# Title of the app
st.title('Conquest Wound Calculator')

col1, col2, col3 = st.columns(3)

with st.sidebar:
    tab1, tab2 = st.tabs(["Active Unit", "Target Unit"])
    with tab1:
        active_unit_input_data = show_active_unit_input()
    with tab2:
        target_unit_input_data = show_target_unit()

engagement_data = EngagementDataModel(
    active_unit_input_data['active_input_target_value'],
    active_unit_input_data['active_input_number_of_attacks_value'],
    active_unit_input_data['active_input_stands'],
    active_unit_input_data['active_input_attacking_stands'],
    st.session_state.special_abilities['active'],
    st.session_state.is_leader,
    target_unit_input_data['target_input_defense_value'],
    target_unit_input_data['target_input_evasion_value'],
    target_unit_input_data['target_input_resolve_value'],
    target_unit_input_data['target_input_stands'],
    st.session_state.special_abilities['target'],
    st.session_state.is_reroll_morale,
    active_unit_input_data['input_action_type']
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
        engagement_data.target_regiment_size_resolve_bonus,
    )

with col3:
    show_results(engagement_data)
