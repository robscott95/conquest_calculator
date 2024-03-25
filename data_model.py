import streamlit as st
import numpy as np

class EngagementDataModel:
    def __init__(
            self,
            active_input_target_value,
            active_input_number_of_attacks_value,
            active_input_stands,
            active_input_attacking_stands,
            active_input_special_abilities,
            target_input_defense_value,
            target_input_evasion_value,
            target_input_resolve_value,
            target_input_stands,
            target_input_special_abilities,
            encounter_params,
        ):
        self.active_input_target_value = active_input_target_value
        self.active_input_number_of_attacks_value = active_input_number_of_attacks_value
        self.active_input_stands = active_input_stands
        self.active_input_attacking_stands = active_input_attacking_stands
        self.target_input_defense_value = target_input_defense_value
        self.target_input_evasion_value = target_input_evasion_value
        self.target_input_resolve_value = target_input_resolve_value
        self.target_input_stands = target_input_stands

        self.encounter_params = encounter_params

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
        
    def _get_rerolls_dict_hits(self):
        rerolls_dict = {
            key.replace("is_to_hits_", ""): ability["value"] for key, ability in self.active_input_special_abilities.items()
            if "is_to_hits_reroll" in key and ability.get("value") is True
        }
        
        # Apply negation logic
        # If is_reroll_misses is True, negate is_reroll_6s
        if 'reroll_misses' in rerolls_dict:
            rerolls_dict.pop('reroll_6s', None)  # Remove 'reroll_6s' if it exists
        
        # If is_reroll_hits is True, negate is_reroll_1s
        if 'reroll_hits' in rerolls_dict:
            rerolls_dict.pop('reroll_1s', None)  # Remove 'reroll_1s' if it exists
        
        return rerolls_dict
    
    def _get_rerolls_dict_defense(self):
        rerolls_dict = {
            key.replace("is_to_defense_", ""): ability["value"] for key, ability in self.target_input_special_abilities.items()
            if "is_to_defense_reroll" in key and ability.get("value") is True
        }
        
        # Apply negation logic
        # If is_reroll_misses is True, negate is_reroll_6s
        if 'reroll_misses' in rerolls_dict:
            rerolls_dict.pop('reroll_6s', None)  # Remove 'reroll_6s' if it exists
        
        # If is_reroll_hits is True, negate is_reroll_1s
        if 'reroll_hits' in rerolls_dict:
            rerolls_dict.pop('reroll_1s', None)  # Remove 'reroll_1s' if it exists
        
        return rerolls_dict

    def _get_rerolls_dict_morale(self):
        rerolls_dict = {
            key.replace("is_to_morale_", ""): ability["value"] for key, ability in self.target_input_special_abilities.items()
            if "is_to_morale_reroll" in key and ability.get("value") is True
        }

        if self.encounter_params['is_flank_attack']:
            rerolls_dict['reroll_misses'] = {'value': True}
        
        # Apply negation logic
        # If is_reroll_misses is True, negate is_reroll_6s
        if 'reroll_misses' in rerolls_dict:
            rerolls_dict.pop('reroll_6s', None)  # Remove 'reroll_6s' if it exists
        
        # If is_reroll_hits is True, negate is_reroll_1s
        if 'reroll_hits' in rerolls_dict:
            rerolls_dict.pop('reroll_1s', None)  # Remove 'reroll_1s' if it exists
        
        return rerolls_dict
        
    def _calc_expected_success(self, number_of_die, target, get_fails=False, reroll_1s=False, reroll_6s=False, reroll_hits=False, reroll_misses=False):

        p_success = target / 6
        p_fail = 1 - p_success

        # Adjust probabilities for rerolling 1s and 6s
        if reroll_6s:
            # If rerolling 6s, effectively reduce the failure probability by the chance of failing and then succeeding.
            p_fail -= (1/6) * p_success
            p_success += (1/6) * p_success

        if reroll_1s:
            # If rerolling 1s, effectively reduce the success probability by the chance of succeeding and then failing.
            p_success -= (1/6) * p_fail
            p_fail += (1/6) * p_fail

        # Calculate initial expected successes and failures
        expected_success = number_of_die * p_success
        expected_fail = number_of_die * p_fail

        # Adjust for rerolling hits or misses
        if reroll_hits:
            # Rerolling hits means taking the expected_success, applying the fail probability, and adding those successes back in
            expected_success -= expected_success * p_fail

        if reroll_misses:
            # Rerolling misses means taking the expected_fail, applying the success probability, and adding those successes
            expected_success += expected_fail * p_success
        
        if get_fails:
            return number_of_die - expected_success

        return expected_success

    @property
    def active_number_of_attacks(self):
        if self.encounter_params['action_type'] == "Clash":
            support_mod =  max(self.active_input_special_abilities['support_mod']['value'], 1)
        elif self.encounter_params['action_type'] == "Volley":
            support_mod = 0
        
        support_to_hits = (self.active_input_supporting_stands * support_mod)
        number_of_attacks = (self.active_input_number_of_attacks_value * self.active_input_attacking_stands)
        number_of_attacks = number_of_attacks + support_to_hits + self.active_input_special_abilities['is_leader']['value']

        if self.active_input_special_abilities['is_double_hits_on_1s']['value']:
            number_of_attacks += number_of_attacks * 1/6

        return number_of_attacks
    
    @property
    def target_resolve(self):
        resolve_value = self.target_input_resolve_value + self.target_regiment_size_resolve_bonus
        if self.target_input_special_abilities['broken']['value']:
            resolve_value = self.target_input_resolve_value

        if self.active_input_special_abilities['resolve_mod']['value'] > 0:
            resolve_value -= self.active_input_special_abilities['resolve_mod']['value']

        return min(resolve_value, 5)

    @property
    def target_to_hit(self):
        target_to_hit = self.active_input_target_value
        if self.active_input_special_abilities['is_inspired']['value']:
            if target_to_hit+1 > 4:
                self.active_input_special_abilities['is_to_hits_reroll_6s']['value'] = True
            else:
                target_to_hit += 1
        return min(target_to_hit, 5)
    
    @property
    def target_defense(self):
        defense_value = self.target_input_defense_value

        if self.target_input_special_abilities['shield']['value'] > 0 and not self.encounter_params['is_flank_attack']:
            defense_value += self.target_input_special_abilities['shield']['value']

        if self.active_input_special_abilities['cleave']['value'] > 0:
            cleave_value = self.active_input_special_abilities['cleave']['value']
            if self.target_input_special_abilities['hardened']['value'] > 0:
                cleave_value -= self.target_input_special_abilities['hardened']['value']
            defense_value -= cleave_value

        highest_defense = max(defense_value, self.target_input_evasion_value)
        return min(highest_defense, 5)

    @property
    def expected_hits(self):
        # unpacking it here not to influence the "rerolls_param" as some target calc funcs can 
        # modify the rerolls dict.
        active_number_of_attacks = self.active_number_of_attacks
        target_to_hit = self.target_to_hit
        rerolls_params = self._get_rerolls_dict_hits()
        return self._calc_expected_success(active_number_of_attacks, target_to_hit, **rerolls_params)

    @property
    def expected_wounds_from_hits(self):
        # unpacking it here not to influence the "rerolls_param" as some target calc funcs can 
        # modify the rerolls dict.
        expected_hits = self.expected_hits
        target_defense = self.target_defense
        rerolls_params = self._get_rerolls_dict_defense()
        return self._calc_expected_success(expected_hits, target_defense, get_fails=True, **rerolls_params)
    
    @property
    def expected_wounds_from_morale(self):
        # unpacking it here not to influence the "rerolls_param" as some target calc funcs can 
        # modify the rerolls dict.
        expected_wounds_from_hits = self.expected_wounds_from_hits
        target_resolve = self.target_resolve
        rerolls_params = self._get_rerolls_dict_morale()
        if self.encounter_params['action_type'] == "Clash":
            expected_wounds = self._calc_expected_success(expected_wounds_from_hits, target_resolve, get_fails=True, **rerolls_params)
        elif self.encounter_params['action_type'] == "Volley":
            expected_wounds = 0
        
        if self.target_input_special_abilities['is_receive_half_morale_wounds']['value']:
            expected_wounds = round(expected_wounds/2, 2)

        return expected_wounds

    @property
    def expected_wounds_from_all(self):
        hit_wounds = self.expected_wounds_from_hits
        morale_wounds = self.expected_wounds_from_morale

        return hit_wounds + morale_wounds

    @staticmethod
    def simulate_dice_rolls(total_number_of_dice, target, simulations=10000, reroll_1s=False, reroll_6s=False, reroll_hits=False, reroll_misses=False):
        rolls = np.random.randint(1, 7, (simulations, total_number_of_dice))

        # Define reroll criteria based on boolean flags
        def reroll_criteria(dice_roll):
            criteria = np.zeros(dice_roll.shape, dtype=bool)
            if reroll_1s:
                criteria |= (dice_roll == 1)
            if reroll_6s:
                criteria |= (dice_roll == 6)
            if reroll_hits:
                criteria |= (dice_roll <= target)
            if reroll_misses:
                criteria |= (dice_roll > target)
            return criteria

        # Apply reroll criteria to initial rolls
        need_reroll = reroll_criteria(rolls)
        
        # Perform rerolls where criteria are met and ensure each die is only rerolled once
        reroll_indices = np.where(need_reroll)
        new_rolls = np.random.randint(1, 7, reroll_indices[0].shape)
        rolls[reroll_indices] = new_rolls

        # Recalculate success counts after rerolls
        success_counts = np.sum(rolls <= target, axis=1)

        unique, counts = np.unique(success_counts, return_counts=True)
        discrete_probabilities = counts / simulations

        full_range = np.arange(1, total_number_of_dice + 1)
        discrete_probabilities_full = np.zeros(total_number_of_dice)
        cumulative_probabilities_full = np.zeros(total_number_of_dice)

        # Fill in the probabilities
        for value, prob in zip(unique, discrete_probabilities):
            if 1 <= value <= total_number_of_dice:
                discrete_probabilities_full[value - 1] = prob

        # Calculate cumulative probabilities
        cumulative_probabilities_full = np.cumsum(discrete_probabilities_full[::-1])[::-1]

        return discrete_probabilities_full, cumulative_probabilities_full, full_range
