import streamlit as st

def calc_expected_hits(number_of_attacks, target, special_abilities):
    p = (target/6)
    expected_hits = number_of_attacks * p
    return expected_hits

# uzyj clopper pearsona do estymacji granic/confidence intervalu
# poniewaz normalne binomialne metody moga sie nie sprawdzic ze wzgledu na maly sample size.