import streamlit as st
from special_abilities import generate_pill_label



def show(defense, evasion, resolve, resolve_bonus):
    st.subheader('Target Unit summary:')
    st.write("Defense: ", defense)
    st.write("Evasion: ", evasion)
    st.write("Resolve: ", resolve)
    st.write("Resolve bonus: ", resolve_bonus)
    
    container = st.container()  # Using container to group pills
    container.write("Special abilities: ")

    for ability, details in st.session_state.special_abilities["target"].items():
        if details['is_modified']:
            # Replace (X) or (+X) with the actual value
            formatted_label = details['label'].replace('(X)', f'({details["value"]})').replace('(+X)', f'(+{details["value"]})')
            
            # Display each modified ability as a pill
            container.markdown(generate_pill_label(formatted_label), unsafe_allow_html=True)