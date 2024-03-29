import streamlit as st
import numpy as np
import math


from stats import Stats

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
            target_input_wounds_per_stand,
            target_input_special_abilities,
            encounter_params
        ):
        self.active_input_target_value = active_input_target_value
        self.active_input_number_of_attacks_value = active_input_number_of_attacks_value
        self.active_input_stands = active_input_stands
        self.active_input_attacking_stands = active_input_attacking_stands
        self.target_input_defense_value = target_input_defense_value
        self.target_input_evasion_value = target_input_evasion_value
        self.target_input_resolve_value = target_input_resolve_value
        self.target_input_stands = target_input_stands
        self.target_input_wounds_per_stand = target_input_wounds_per_stand

        self.encounter_params = encounter_params

        self.active_input_special_abilities = active_input_special_abilities
        self.target_input_special_abilities = target_input_special_abilities

        self.active_input_supporting_stands = active_input_stands - active_input_attacking_stands

        self.stats = Stats()
    
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
        return self.stats.calc_expected_success(active_number_of_attacks, target_to_hit, **rerolls_params)

    @property
    def expected_wounds_from_hits(self):
        # unpacking it here not to influence the "rerolls_param" as some target calc funcs can 
        # modify the rerolls dict.
        expected_hits = self.expected_hits
        target_defense = self.target_defense
        rerolls_params = self._get_rerolls_dict_defense()
        return self.stats.calc_expected_success(expected_hits, target_defense, get_fails=True, **rerolls_params)
    
    @property
    def expected_wounds_from_morale(self):
        # unpacking it here not to influence the "rerolls_param" as some target calc funcs can 
        # modify the rerolls dict.
        expected_wounds_from_hits = self.expected_wounds_from_hits
        target_resolve = self.target_resolve
        rerolls_params = self._get_rerolls_dict_morale()
        if self.encounter_params['action_type'] == "Clash":
            expected_wounds = self.stats.calc_expected_success(expected_wounds_from_hits, target_resolve, get_fails=True, **rerolls_params)
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

    @property
    def target_wounds_total(self):
        return self.target_input_wounds_per_stand * self.target_input_stands

    @property
    def expected_remaining_wounds(self):
        return self.target_wounds_total - self.expected_wounds_from_all
    
    @property
    def expected_stands_remaining(self):
        return self.expected_remaining_wounds / self.target_input_stands
    
    @property
    def expected_wounds_remaining_on_last_stand(self):
        return self.expected_remaining_wounds - (math.floor(self.expected_stands_remaining) * self.target_input_wounds_per_stand)
    
    def get_killed_stands(self, wounds):
        return math.floor(wounds / self.target_input_wounds_per_stand)