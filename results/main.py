import streamlit as st
from data_model import EngagementDataModel

def show(engagement_data: EngagementDataModel):
    st.header("Results")

    st.subheader('Rolling to Hit:')
    st.write('Number of attacks:', engagement_data.active_number_of_attacks)
    st.write('Expected number of hits:', engagement_data.expected_hits)


    st.subheader('Defense roll:')
    # calc number of die rolled
    # check if we need support at 1 or 0
    st.write("Expected wounds: ", engagement_data.expected_wounds) 

