import streamlit as st
from views.special_abilities.summary import show as show_summary_special_abilities



def show(defense, evasion, resolve, resolve_bonus, target_special_abilities):
    with st.container(border=True):
        st.subheader('Target Unit summary:')
        st.write("Defense: ", defense)
        st.write("Evasion: ", evasion)
        st.write("Resolve: ", resolve)
        st.write("Resolve bonus: ", resolve_bonus)

        with st.container(border=True):
            show_summary_special_abilities(target_special_abilities)