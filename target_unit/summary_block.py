import streamlit as st
from common_util import generate_pill_label

def show(defense, evasion, resolve, number_of_stands):
    st.subheader('Stats summary:')
    print(st.session_state.special_abilities)
    final_defense = defense - st.session_state.special_abilities['active']['cleave']['value']
    st.write("Defense: ", final_defense)
    st.write("Evasion: ", evasion)
    final_resolve = number_of_stands * 1
    st.write("Resolve: ", resolve)
    
    container = st.container()  # Using container to group pills
    container.write("Special abilities: ")

    for ability, details in st.session_state.special_abilities["target"].items():
        if details['is_modified']:
            # Replace (X) or (+X) with the actual value
            formatted_label = details['label'].replace('(X)', f'({details["value"]})').replace('(+X)', f'(+{details["value"]})')
            
            # Display each modified ability as a pi
            container.markdown(generate_pill_label(formatted_label), unsafe_allow_html=True)