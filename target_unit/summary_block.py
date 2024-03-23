import streamlit as st
from common_util import generate_pill_label

def calculate_additional_resolve(number_of_stands):
    if 4 <= number_of_stands <= 6:
        return 1
    elif 7 <= number_of_stands <= 9:
        return 2
    elif 9 <= number_of_stands:
        return 3
    else:
        return 0

def show(defense, evasion, resolve, number_of_stands):
    st.subheader('Stats summary:')
    st.session_state.final_defense = defense - st.session_state.special_abilities['active']['cleave']['value']
    st.write("Defense: ", st.session_state.final_defense)
    st.write("Evasion: ", evasion)
    st.session_state.final_resolve = min(resolve + calculate_additional_resolve(number_of_stands), 5)
    st.write("Resolve: ", st.session_state.final_resolve)
    
    container = st.container()  # Using container to group pills
    container.write("Special abilities: ")

    for ability, details in st.session_state.special_abilities["target"].items():
        if details['is_modified']:
            # Replace (X) or (+X) with the actual value
            formatted_label = details['label'].replace('(X)', f'({details["value"]})').replace('(+X)', f'(+{details["value"]})')
            
            # Display each modified ability as a pi
            container.markdown(generate_pill_label(formatted_label), unsafe_allow_html=True)