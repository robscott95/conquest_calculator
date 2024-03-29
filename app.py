import streamlit as st
from views.active_unit.input import show as show_active_unit_input
from views.active_unit.summary import show as show_active_unit_summary
from views.target_unit.input import show as show_target_unit_input
from views.target_unit.summary import show as show_target_unit_summary
from views.results.summary import show as show_results
from views.encounter_params.input import show as show_encounter_params_input


from data_model import EngagementDataModel
from roll_visualizer import VisualizeRollEstimation

import seaborn as sns
import matplotlib.pyplot as plt

import time

# Title of the app
st.title('Conquest Wound Calculator')

with st.sidebar:
    st.header("Options")
    encounter_params = show_encounter_params_input()

    st.subheader("Stand params")
    tab1, tab2 = st.tabs(["Active Unit", "Target Unit"])

    with tab1:
        active_unit_input_data = show_active_unit_input()
    with tab2:
        target_unit_input_data = show_target_unit_input()

engagement_data = EngagementDataModel(
    active_unit_input_data['active_input_target_value'],
    active_unit_input_data['active_input_number_of_attacks_value'],
    active_unit_input_data['active_input_stands'],
    active_unit_input_data['active_input_attacking_stands'],
    active_unit_input_data['active_input_special_abilities'],
    target_unit_input_data['target_input_defense_value'],
    target_unit_input_data['target_input_evasion_value'],
    target_unit_input_data['target_input_resolve_value'],
    target_unit_input_data['target_input_stands'],
    target_unit_input_data['target_input_wounds_per_stand'],
    target_unit_input_data['target_input_special_abilities'],
    encounter_params
)

visualizer = VisualizeRollEstimation(engagement_data)
fig = visualizer.visualize_expected_hits_and_morale()
config = {
    'staticPlot': False,  # Allows hover effects but prevents zoom, pan, etc.
    'scrollZoom': False,  # Disables zooming with scroll
    'showLink': False,  # Hides the link to edit chart on Plotly,
    'displayModeBar': False
}
st.plotly_chart(fig, use_container_width=True, config=config)

fig = visualizer.visualize_simulated_all()
st.plotly_chart(fig, use_container_width=True, config=config)

col1, col2, col3 = st.columns(3)
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
        engagement_data.target_input_special_abilities
    )

with col3:
    show_results(engagement_data)
