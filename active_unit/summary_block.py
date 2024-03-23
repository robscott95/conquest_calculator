import streamlit as st
from util import generate_pill_label

def show(target, no_of_die, no_of_stands_engaged, no_of_stands_all):
    st.subheader('Stats summary:')
    st.write("Target value: ", target)
    st.write("Attack/Barrage: ", no_of_die)
    st.write("Engaged stands: ", no_of_stands_engaged)
    st.write("Supporting stands: ", no_of_stands_all - no_of_stands_engaged)
    modified_abilities = [key for key, value in st.session_state.special_abilities_values.items() if value.get("is_modified", False)]

    if modified_abilities:
        st.markdown("Special abilities: ", unsafe_allow_html=True)
        for ability in modified_abilities:
            # Display each modified ability as a pill label
            ability_label = st.session_state.special_abilities_values[ability].get("label", ability)  # Fallback to the key if label not present
            # ability_label = ability_label.
            st.markdown(generate_pill_label(ability_label), unsafe_allow_html=True)
    else:
        st.write("No special effects modified.")