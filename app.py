import streamlit as st
from active_unit.main import show as show_active_unit
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title('Conquest Wound Calculator')


col1, col2, col3 = st.columns(3)

with col1:
    unit_stats_data = show_active_unit()
