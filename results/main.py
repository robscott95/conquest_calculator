import streamlit as st
from data_model import EngagementDataModel

def show(engagement_data: EngagementDataModel):
    st.header("Results")

    st.subheader('Rolling to Hit:')
    st.write('Number of attacks:', engagement_data.active_number_of_attacks)
    st.write('Expected number of hits:', round(engagement_data.expected_hits, 2))

    st.subheader('Defense roll:')
    st.write("Expected wounds: ", round(engagement_data.expected_wounds_from_hits, 2)) 

    st.subheader('Morale test:')
    st.write("Expected wounds: ", round(engagement_data.expected_wounds_from_morale, 2))

    st.subheader('Summary: ')
    st.write("Expected total wounds: ", round(engagement_data.expected_wounds_from_all, 2))

