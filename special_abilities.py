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

def show_input(unit_type):
    # Load special abilities from a JSON file if not already loaded
    if 'special_abilities' not in st.session_state:
        st.session_state.special_abilities = {}

    if unit_type not in st.session_state.special_abilities:
        with open(f'{unit_type}_unit/special_abilities.json', 'r') as f:
            st.session_state.special_abilities[unit_type] = json.load(f)
            for ability in st.session_state.special_abilities[unit_type].keys():
                st.session_state.special_abilities[unit_type][ability]["is_modified"] = False

    # Multiselect for choosing special abilities
    labels_to_keys = {details['label']: key for key, details in st.session_state.special_abilities[unit_type].items()}
    abilities_labels = list(labels_to_keys.keys())
    selected_abilities = st.multiselect("Choose special abilities:", abilities_labels, key=f"{unit_type}_multiselect")
    selected_abilities = [labels_to_keys[ability] for ability in selected_abilities]

    # Function to create an input widget for each ability
    def special_ability_input(key, label, input_type='number'):
        widget_key = f"{unit_type}_{key}"
        current_value = st.session_state.special_abilities[unit_type][key]['value']
        
        if input_type == 'number':
            new_value = st.number_input(label, min_value=0, key=widget_key)
        elif input_type == 'checkbox':
            new_value = st.checkbox(label, key=widget_key)
        
        if current_value != new_value:
            st.session_state.special_abilities[unit_type][key]['value'] = new_value
            st.session_state.special_abilities[unit_type][key]['is_modified'] = True

    # Display input widgets for selected or modified abilities
    for ability in selected_abilities:
        details = st.session_state.special_abilities[unit_type][ability]
        input_type = 'checkbox' if isinstance(details['value'], bool) else 'number'
        special_ability_input(ability, details['label'], input_type=input_type)

    for ability, details in st.session_state.special_abilities[unit_type].items():
        if details['is_modified'] and ability not in selected_abilities:
            input_type = 'checkbox' if isinstance(details['value'], bool) else 'number'
            special_ability_input(ability, details['label'], input_type=input_type)

    # Always visible checkbox for "Leader"
    if unit_type == "active":
        st.session_state.is_leader = st.checkbox('Leader', value=True)
    if unit_type == "target":
        st.session_state.is_reroll_morale = st.checkbox('Re-roll morale saves', value=False)

def show_summary(unit_type):
    container = st.container()  # Using container to group pills
    container.write("Special abilities: ")

    for ability, details in st.session_state.special_abilities[unit_type].items():
        if details['is_modified']:
            # Replace (X) or (+X) with the actual value
            formatted_label = details['label'].replace('(X)', f'({details["value"]})').replace('(+X)', f'(+{details["value"]})')
            
            # Display each modified ability as a pi
            container.markdown(generate_pill_label(formatted_label), unsafe_allow_html=True)

    if unit_type == "active" and st.session_state.is_leader:
        container.markdown(generate_pill_label("Leader"), unsafe_allow_html=True)
