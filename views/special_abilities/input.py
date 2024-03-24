import json
import streamlit as st

def load_special_abilities(unit_type):
    try:
        with open(f'views/{unit_type}_unit/special_abilities.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def show(unit_type):
    # Load special abilities into a local variable
    special_abilities = load_special_abilities(unit_type)

    # Separate always_visible abilities from the rest
    always_visible_abilities = {k: v for k, v in special_abilities.items() if v.get('always_visible', False)}
    selectable_abilities = {k: v for k, v in special_abilities.items() if not v.get('always_visible', False)}

    # Generate labels to keys mapping for selectable abilities
    labels_to_keys = {details['label']: key for key, details in selectable_abilities.items()}
    abilities_labels = list(labels_to_keys.keys())

    # Multiselect for choosing special abilities (excluding always_visible abilities)
    selected_labels = st.multiselect("Choose special abilities:", abilities_labels, key=f"{unit_type}_multiselect")
    selected_keys = [labels_to_keys[label] for label in selected_labels]

    # Define the input widget creation function
    def special_ability_input(key, details, input_type='number'):
        widget_key = f"{unit_type}_{key}"
        current_value = details['value']
        if input_type == 'number':
            new_value = st.number_input(details['label'], min_value=0, value=current_value, key=widget_key)
        elif input_type == 'checkbox':
            new_value = st.checkbox(details['label'], value=current_value, key=widget_key)
        details['value'] = new_value

    # Display widgets for always visible abilities
    for key, details in always_visible_abilities.items():
        input_type = 'checkbox' if isinstance(details['value'], bool) else 'number'
        special_ability_input(key, details, input_type=input_type)

    # Display widgets for selected abilities or those with non-zero values (excluding always_visible)
    for key in selected_keys:
        details = selectable_abilities[key]
        input_type = 'checkbox' if isinstance(details['value'], bool) else 'number'
        special_ability_input(key, details, input_type=input_type)

    # Combine always_visible and selectable abilities back into special_abilities
    special_abilities.update(always_visible_abilities)
    special_abilities.update(selectable_abilities)

    # Return updated special abilities
    return special_abilities