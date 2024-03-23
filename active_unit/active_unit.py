# unit_stats.py
import streamlit as st
import json

def show():
    st.header("Active unit's stat block:")

    # Collapsible section for Unit Stats
    with st.expander("Unit Stats", expanded=True):
        target = st.slider('Target value (Clash / Volley)', min_value=1, max_value=6, value=3)
        no_of_die = st.slider('No of die (Attacks / Barrage)', min_value=1, max_value=20, value=4)
        no_of_stands_all = st.slider('No of Stands', min_value=1, max_value=20, value=3)
        no_of_stands_engaged = st.slider('No of Engaged Stands', min_value=0, max_value=no_of_stands_all, value=min(no_of_stands_all, 4))

    # Load and initialize session state for storing values and tracking modifications if not already present
    if 'special_abilities_values' not in st.session_state:
        with open('active_unit/special_abilities.json', 'r') as f:
            st.session_state.special_abilities_values = json.load(f)
            for ability in st.session_state.special_abilities_values.keys():
                st.session_state.special_abilities_values[ability]["is_modified"] = False

    # Collapsible section for Special Abilities
    with st.expander("Special Abilities", expanded=True):
        # Always visible
        is_leader = st.checkbox('Leader', value=True)

        # Function to create an input widget based on the type and update session state
        def special_ability_input(key, label, value, input_type='number'):
            current_value = st.session_state.special_abilities_values[key]['value']
            if input_type == 'number':
                new_value = st.number_input(label, min_value=0, value=current_value, key=key)
            elif input_type == 'checkbox':
                new_value = st.checkbox(label, value=current_value, key=key)
            
            if current_value != new_value:
                st.session_state.special_abilities_values[key]['value'] = new_value
                st.session_state.special_abilities_values[key]['is_modified'] = True

        # Define the search term input
        search_term = st.text_input("Search...").lower().strip()

        # Display widgets dynamically based on search input or if they have been modified
        if len(search_term) > 0:
            for ability, details in st.session_state.special_abilities_values.items():
                if search_term in ability.lower() or search_term in details['label'].lower() or st.session_state.special_abilities_values[ability]['is_modified']:
                    input_type = 'checkbox' if isinstance(details['value'], bool) else 'number'
                    special_ability_input(ability, details['label'], details['value'], input_type=input_type)
        else:
            # Show modified options by default
            for ability, details in st.session_state.special_abilities_values.items():
                if st.session_state.special_abilities_values[ability]['is_modified']:
                    input_type = 'checkbox' if isinstance(details['value'], bool) else 'number'
                    special_ability_input(ability, details['label'], details['value'], input_type=input_type)

    # Calculation and display area outside of collapsible context, responsive to input changes
    st.subheader('Submitted Unit Stats:')
    support_to_hits = ((no_of_stands_all - no_of_stands_engaged) * max(st.session_state.special_abilities_values['support_mod']['value'], 1))
    number_of_die_to_roll = (no_of_die * no_of_stands_engaged) + is_leader + support_to_hits
    st.write("Target value: ", target)
    st.write('Number of die rolled:', number_of_die_to_roll)