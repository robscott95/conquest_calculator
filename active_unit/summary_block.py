import streamlit as st
from util import generate_pill_label

def show(target, no_of_die, no_of_stands_engaged, no_of_stands_all):
    st.subheader('Stats summary:')
    st.write("Target value: ", target)
    st.write("Attack/Barrage: ", no_of_die)
    st.write("Engaged stands: ", no_of_stands_engaged)
    st.write("Supporting stands: ", no_of_stands_all - no_of_stands_engaged)
    
    container = st.container()  # Using container to group pills
    container.write("Special abilities: ")

    for ability, details in st.session_state.special_abilities_values.items():
        if details['is_modified']:
            # Replace (X) or (+X) with the actual value
            formatted_label = details['label'].replace('(X)', f'({details["value"]})').replace('(+X)', f'(+{details["value"]})')
            
            # Display each modified ability as a pi
            container.markdown(generate_pill_label(formatted_label), unsafe_allow_html=True)