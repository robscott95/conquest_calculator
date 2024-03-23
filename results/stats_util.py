import streamlit as st

def calc_expected_success(number_of_die, target):
    p = (target/6)
    expected_success = number_of_die * p
    return expected_success

def calc_expected_hits(attacks, hit_target, special_abilities):
    return calc_expected_success(attacks, hit_target)


def calc_expected_wounds(hits, defense_target, special_abilities):
    return calc_expected_success(hits, defense_target)

# uzyj clopper pearsona do estymacji granic/confidence intervalu
# poniewaz normalne binomialne metody moga sie nie sprawdzic ze wzgledu na maly sample size.
