import json
import streamlit as st

def generate_pill_label(text):
    pill_html = f"""
    <style>
    .pill {{
        margin: 2px;
        display: inline-block;
        padding: 0px 10px;
        border-radius: 15px;
        background-color: #0d6efd;
        color: white;
        font-size: 14px;
        line-height: 22px;
    }}
    </style>
    <span class="pill">{text}</span>
    """
    return pill_html

# def initialize_

def show_special_abilities_block(unit_type):
    if 'special_abilities_values' not in st.session_state:
        st.session_state.special_abilities_values = {}

    if unit_type not in st.session_state.special_abilities_values:
        with open(f'{unit_type}_unit/special_abilities.json', 'r') as f:
            st.session_state.special_abilities_values[unit_type] = json.load(f)
            for ability in st.session_state.special_abilities_values[unit_type].keys():
                st.session_state.special_abilities_values[unit_type][ability]["is_modified"] = False

    # Always visible
    if unit_type == "active":
        st.session_state.is_leader = st.checkbox('Leader', value=True)

    # Function to create an input widget based on the type and update session state
    def special_ability_input(key, label, input_type='number'):
        widget_key = f"{unit_type}_{key}"  # Example of making the key more unique
        current_value = st.session_state.special_abilities_values[unit_type][key]['value']
        if input_type == 'number':
            # Use the modified widget_key
            new_value = st.number_input(label, min_value=0, key=widget_key)
        elif input_type == 'checkbox':
            # Use the modified widget_key
            new_value = st.checkbox(label, key=widget_key)
        
        if current_value != new_value:
            st.session_state.special_abilities_values[unit_type][key]['value'] = new_value
            if new_value != 0:
                st.session_state.special_abilities_values[unit_type][key]['is_modified'] = True
            else:
                st.session_state.special_abilities_values[unit_type][key]['is_modified'] = False

    # Define the search term input
    search_term = st.text_input("Search...", key=f"{unit_type}_search").lower().strip()

    # Display widgets dynamically based on search input or if they have been modified
    if len(search_term) > 0:
        for ability, details in st.session_state.special_abilities_values[unit_type].items():
            if search_term in ability.lower() or search_term in details['label'].lower() or details['is_modified']:
                input_type = 'checkbox' if isinstance(details['value'], bool) else 'number'
                special_ability_input(ability, details['label'], input_type=input_type)
    else:
        # Show modified options by default
        for ability, details in st.session_state.special_abilities_values[unit_type].items():
            if details['is_modified']:
                input_type = 'checkbox' if isinstance(details['value'], bool) else 'number'
                special_ability_input(ability, details['label'], input_type=input_type)

def show_special_ability_summary_block(unit_type):
    container = st.container()  # Using container to group pills
    container.write("Special abilities: ")

    for ability, details in st.session_state.special_abilities_values[unit_type].items():
        if details['is_modified']:
            # Replace (X) or (+X) with the actual value
            formatted_label = details['label'].replace('(X)', f'({details["value"]})').replace('(+X)', f'(+{details["value"]})')
            
            # Display each modified ability as a pi
            container.markdown(generate_pill_label(formatted_label), unsafe_allow_html=True)
