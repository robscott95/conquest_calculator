import streamlit as st
from results.stats_util import calc_expected_hits, calc_expected_wounds

def show():
    st.header("Results")

    st.subheader('To hit:')
    # calc number of die rolled
    # check if we need support at 1 or 0
    if st.session_state.action_type=="Clash":
        support_mod =  max(st.session_state.special_abilities['active']['support_mod']['value'], 1)
    elif st.session_state.action_type == "Volley":
        support_mod = 0
    support_to_hits = ((st.session_state.no_of_stands_all - st.session_state.no_of_stands_engaged) * support_mod)
    number_of_attacks = (st.session_state.no_of_attacks * st.session_state.no_of_stands_engaged) + st.session_state.is_leader + support_to_hits
    expected_hits = calc_expected_hits(number_of_attacks, st.session_state.target_attack, st.session_state.special_abilities)
    st.write('Number of attacks:', number_of_attacks)
    st.write('Expected number of hits:', expected_hits)


    st.subheader('Defense roll:')
    # calc number of die rolled
    # check if we need support at 1 or 0
    # st.write("Expected wounds: ", calc_expected_wounds(expected_hits, )) 

