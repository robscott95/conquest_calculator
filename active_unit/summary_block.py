import streamlit as st
from common_util import show_special_ability_summary_block

def show(target, no_of_die, no_of_stands_engaged, no_of_stands_all):
    st.subheader('Stats summary:')
    st.write("Target value: ", target)
    st.write("Attack/Barrage: ", no_of_die)
    st.write("Engaged stands: ", no_of_stands_engaged)
    st.write("Supporting stands: ", no_of_stands_all - no_of_stands_engaged)
    
    show_special_ability_summary_block("active")