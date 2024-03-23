import streamlit as st
from active_unit.main import show as show_active_unit
from target_unit.main import show as show_target_unit
from results.main import show as show_results

import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title('Conquest Wound Calculator')


col1, col2, col3 = st.columns(3)

with col1:
    show_active_unit()

with col2:
    show_target_unit()

with col3:
    show_results()