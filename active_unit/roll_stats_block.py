import streamlit as st
from stats_util import calc_expected_hits

def show(no_of_attacks, no_of_stands_all, no_of_stands_engaged, action):
    st.subheader('Roll stats:')
    # calc number of die rolled
    # check if we need support at 1 or 0
    if action=="Clash":
        support_mod =  max(st.session_state.special_abilities_values['active']['support_mod']['value'], 1)
    elif action == "Volley":
        support_mod = 0
    support_to_hits = ((no_of_stands_all - no_of_stands_engaged) * support_mod)
    number_of_die_to_roll = (no_of_attacks * no_of_stands_engaged) + st.session_state.is_leader + support_to_hits
    st.write('Number of die rolled:', number_of_die_to_roll)


    st.write('Expected number of hits:', calc_expected_hits())