import streamlit as st

def calc_expected_hits(number_of_attacks, target, special_abilities):
    expected_hits = number_of_attacks * (target/6)
    return expected_hits
