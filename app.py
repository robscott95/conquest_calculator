import streamlit as st
from active_unit.active_unit import show as show_active_unit
import seaborn as sns
import matplotlib.pyplot as plt


def update_special_ability(key, widget_func):
    st.session_state.special_abilities_values[key] = widget_func()

# Title of the app
st.title('Conquest Wound Calculator')


col1, col2, col3 = st.columns(3)

with col1:
    unit_stats_data = show_active_unit()
