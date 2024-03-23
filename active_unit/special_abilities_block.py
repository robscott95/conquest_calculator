import streamlit as st

def show():
    # Always visible
        st.session_state.is_leader = st.checkbox('Leader', value=True)

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