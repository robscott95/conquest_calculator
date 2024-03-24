# unit_stats.py
import streamlit as st

from special_abilities import show_input as show_input_special_abilities

def show(
    initial_target_attack=3,
    initial_no_of_attacks=4,
    initial_no_of_stands_all=3,
    initial_no_of_stands_engaged=3
):
    st.header("Active unit:")
    # Collapsible section for Unit Stats
    with st.expander("Unit Stats", expanded=True):
        target_attack = st.slider('Target value', min_value=1, max_value=6, value=initial_target_attack)
        no_of_attacks = st.slider('Attacks value', min_value=1, max_value=20, value=initial_no_of_attacks)
        no_of_stands_all = st.slider('Stands', min_value=1, max_value=20, value=initial_no_of_stands_all)
        no_of_stands_engaged = st.slider('Attacking Stands', min_value=0, max_value=no_of_stands_all, value=initial_no_of_stands_engaged)

    # Collapsible section for Special Abilities
    # Assuming show_special_abilities_block returns a dict or similar structure of the selected abilities
    with st.expander("Special Abilities", expanded=True):
        special_abilities = show_input_special_abilities("active")

    action_type = st.radio("Action:", ["Clash", "Volley"])

    # Return all relevant values
    return {
        "active_input_target_value": target_attack,
        "active_input_number_of_attacks_value": no_of_attacks,
        "active_input_stands": no_of_stands_all,
        "active_input_attacking_stands": no_of_stands_engaged,
        "active_input_special_abilities": special_abilities,  # This depends on your implementation
        "input_action_type": action_type
    }
