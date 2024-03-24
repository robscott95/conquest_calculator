import streamlit as st
from special_abilities import show_special_ability_summary_block

def show(target, number_of_attacks, number_of_attacking_stands, number_of_supporting_stands, active_special_abilities):
    st.subheader('Active Unit summary:')
    st.write("Target value: ", target)
    st.write("Number of attacks: ", number_of_attacks)
    st.write("Engaged stands: ", number_of_attacking_stands)
    st.write("Supporting stands: ", number_of_supporting_stands)
    
    show_special_ability_summary_block("active")