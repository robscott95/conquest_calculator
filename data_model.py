import streamlit as st

class EngagementDataModel:
    def __init__(
            self,
            active_input_target_value,
            active_input_number_of_attacks_value,
            active_input_stands,
            active_input_attacking_stands,
            active_input_special_abilities,
            active_input_is_leader_present,
            target_input_defense_value,
            target_input_evasion_value,
            target_input_resolve_value,
            target_input_stands,
            target_input_special_abilities,
            target_input_is_engaged_on_flank,
            input_action_type,
        ):
        self.active_input_target_value = active_input_target_value
        self.active_input_number_of_attacks_value = active_input_number_of_attacks_value
        self.active_input_stands = active_input_stands
        self.active_input_attacking_stands = active_input_attacking_stands
        self.active_input_is_leader_present = active_input_is_leader_present
        self.target_input_defense_value = target_input_defense_value
        self.target_input_evasion_value = target_input_evasion_value
        self.target_input_resolve_value = target_input_resolve_value
        self.target_input_stands = target_input_stands
        self.target_input_is_engaged_on_flank = target_input_is_engaged_on_flank

        self.input_action_type = input_action_type

        self.active_input_special_abilities = active_input_special_abilities
        self.target_input_special_abilities = target_input_special_abilities

        self.active_input_supporting_stands = active_input_stands - active_input_attacking_stands
    
    @property
    def target_regiment_size_resolve_bonus(self):
        if 4 <= self.target_input_stands <= 6:
            return 1
        elif 7 <= self.target_input_stands <= 9:
            return 2
        elif 9 <= self.target_input_stands:
            return 3
        else:
            return 0
        
    def _calc_expected_success(self, number_of_die, target, invert_p=False, reroll_1s=False, reroll_6s=False, reroll_hits=False, reroll_misses=False):
        p_success = target / 6
        p_fail = 1 - p_success

        if invert_p:
            p_success, p_fail = p_fail, p_success

        # Adjust probabilities for rerolling 1s and 6s
        if reroll_1s:
            # If rerolling 1s, effectively reduce the failure probability by the chance of failing and then succeeding.
            p_fail -= (1/6) * p_success
            p_success += (1/6) * p_success

        if reroll_6s:
            # If rerolling 6s, effectively reduce the success probability by the chance of succeeding and then failing.
            p_success -= (1/6) * p_fail
            p_fail += (1/6) * p_fail

        # Calculate initial expected successes and failures
        expected_success = number_of_die * p_success
        expected_fail = number_of_die * p_fail

        # Adjust for rerolling hits or misses
        if reroll_hits:
            # Rerolling hits means taking the expected_success, applying the fail probability, and adding those successes back in
            expected_success += expected_success * p_fail

        if reroll_misses:
            # Rerolling misses means taking the expected_fail, applying the success probability, and adding those successes
            expected_success += expected_fail * p_success

        return expected_success

    @property
    def active_number_of_attacks(self):
        if self.input_action_type == "Clash":
            support_mod =  max(self.active_input_special_abilities['support_mod']['value'], 1)
        elif self.input_action_type == "Volley":
            support_mod = 0
        support_to_hits = (self.active_input_supporting_stands * support_mod)
        number_of_attacks = (self.active_input_number_of_attacks_value * self.active_input_attacking_stands) + st.session_state.is_leader + support_to_hits
        return number_of_attacks

    @property
    def expected_hits(self):
        return self._calc_expected_success(self.active_number_of_attacks, self.active_input_target_value)

    @property
    def expected_wounds_from_hits(self):
        final_defense_value = max(self.target_input_defense_value, self.target_input_evasion_value)
        return self._calc_expected_success(self.expected_hits, final_defense_value, invert_p=True)
    
    @property
    def expected_wounds_from_morale(self):
        if self.input_action_type == "Clash":
            resolve_target = self.target_input_resolve_value + self.target_regiment_size_resolve_bonus
            return self._calc_expected_success(self.expected_wounds_from_hits, resolve_target, invert_p=True)
        elif self.input_action_type == "Volley":
            return 0
        

    @property
    def expected_wounds_from_all(self):
        hit_wounds = self.expected_wounds_from_hits
        morale_wounds = self.expected_wounds_from_morale

        return hit_wounds + morale_wounds
    




