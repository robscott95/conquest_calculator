import numpy as np
import math

class Stats:
    def __init__(self):
        pass

    def calc_expected_success(self, number_of_die, target, get_fails=False, reroll_1s=False, reroll_6s=False, reroll_hits=False, reroll_misses=False):

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
    
    def simulate_dice_rolls(self, total_number_of_dice, target, simulations=10000, reroll_1s=False, reroll_6s=False, reroll_hits=False, reroll_misses=False):
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
        reroll_indices = np.where(need_reroll)
        new_rolls = np.random.randint(1, 7, reroll_indices[0].shape)
        rolls[reroll_indices] = new_rolls

        # Recalculate success counts after rerolls
        success_counts = np.sum(rolls <= target, axis=1)
        fail_counts = total_number_of_dice - success_counts

        # Calculate probabilities for success
        unique_success, counts_success = np.unique(success_counts, return_counts=True)
        discrete_probabilities_success = counts_success / simulations
        full_range = np.arange(0, total_number_of_dice + 1)
        discrete_probabilities_success_full = np.zeros(total_number_of_dice + 1)
        cumulative_probabilities_success_full = np.zeros(total_number_of_dice + 1)
        for value, prob in zip(unique_success, discrete_probabilities_success):
            discrete_probabilities_success_full[value] = prob
        cumulative_probabilities_success_full = np.cumsum(discrete_probabilities_success_full[::-1])[::-1]

        # Calculate probabilities for fails
        unique_fail, counts_fail = np.unique(fail_counts, return_counts=True)
        discrete_probabilities_fail = counts_fail / simulations
        discrete_probabilities_fail_full = np.zeros(total_number_of_dice + 1)
        cumulative_probabilities_fail_full = np.zeros(total_number_of_dice + 1)
        for value, prob in zip(unique_fail, discrete_probabilities_fail):
            discrete_probabilities_fail_full[value] = prob
        cumulative_probabilities_fail_full = np.cumsum(discrete_probabilities_fail_full[::-1])[::-1]

        results = {
            "success": {
                "counts": success_counts,
                "unique": unique_success,
                "full_range": full_range,
                "discrete_probabilities": discrete_probabilities_success_full, 
                "cumulative_probabilities": cumulative_probabilities_success_full, 
            },
            "fails": {
                "counts": fail_counts,
                "unique": unique_fail,
                "full_range": full_range,
                "discrete_probabilities": discrete_probabilities_fail_full, 
                "cumulative_probabilities": cumulative_probabilities_fail_full, 
            }
        }
        print(results)
        return results
    
    def get_simulation_params(self, data, mode):
        if mode == "hits":
            reroll_params = data._get_rerolls_dict_hits()
            total_number_of_dice = data.active_number_of_attacks
            target = data.target_to_hit

        elif mode == "defense":
            reroll_params = data._get_rerolls_dict_defense()
            total_number_of_dice = data.expected_hits
            target = data.target_defense
        elif mode == "morale":
            reroll_params = data._get_rerolls_dict_morale()
            total_number_of_dice = data.expected_wounds_from_hits
            if data.encounter_params['action_type'] == "Volley":
                target = 6
            else:
                target = data.target_resolve

        return reroll_params, total_number_of_dice, target


    def simulate_rolls_by_type(self, data, mode):
        reroll_params, total_number_of_dice, target = self.get_simulation_params(data, mode)

        if mode in ["defense", "morale"]:
            previous_mode = "hits" if mode == "defense" else "defense"
            previous_simulation_results = self.simulate_rolls_by_type(data, previous_mode)
            max_full_range = max(previous_simulation_results["success"]["full_range"])
            
            # Initialize aggregated probabilities arrays
            aggregated_discrete_probabilities_success = np.zeros(max_full_range + 1)
            aggregated_cumulative_probabilities_success = np.zeros(max_full_range + 1)
            aggregated_discrete_probabilities_fails = np.zeros(max_full_range + 1)
            aggregated_cumulative_probabilities_fails = np.zeros(max_full_range + 1)
            
            states = ['success', 'fails']
            # Aggregate results based on the distribution of previous phase outcomes
            for state in states:
                for outcome, probability in zip(previous_simulation_results[state]["full_range"], previous_simulation_results[state]["discrete_probabilities"]):
                    if probability > 0:  # Only simulate for outcomes that occurred
                        current_results = self.simulate_dice_rolls(
                            outcome, target, simulations=10000, **reroll_params  # Simulate based on the outcome as total dice
                        )

                        # Update max full range if necessary
                        current_max_full_range = len(current_results[state]["discrete_probabilities"])
                        max_full_range = max(max_full_range, current_max_full_range - 1)
                        
                        # Weight discrete probabilities by the probability of the outcome occurring
                        weighted_discrete_probabilities = current_results[state]["discrete_probabilities"] * probability
                        
                        # Extend aggregated arrays if necessary
                        if len(aggregated_discrete_probabilities_success) < len(weighted_discrete_probabilities):
                            extra_zeros = np.zeros(len(weighted_discrete_probabilities) - len(aggregated_discrete_probabilities_success))
                            aggregated_discrete_probabilities_success = np.concatenate((aggregated_discrete_probabilities_success, extra_zeros))
                            aggregated_discrete_probabilities_fails = np.concatenate((aggregated_discrete_probabilities_fails, extra_zeros))
                        
                        # Aggregate weighted probabilities into the total distribution
                        if state == 'success':
                            aggregated_discrete_probabilities_success[:len(weighted_discrete_probabilities)] += weighted_discrete_probabilities
                        else:
                            aggregated_discrete_probabilities_fails[:len(weighted_discrete_probabilities)] += weighted_discrete_probabilities

            # Calculate cumulative probabilities
            aggregated_cumulative_probabilities_success = np.cumsum(aggregated_discrete_probabilities_success[::-1])[::-1]
            aggregated_cumulative_probabilities_fails = np.cumsum(aggregated_discrete_probabilities_fails[::-1])[::-1]
            
            # Create aggregated full range array
            aggregated_full_range = np.arange(0, max_full_range+1)
            
            # Combine aggregated results
            simulation_results = {
                "success": {
                    "full_range": aggregated_full_range,
                    "discrete_probabilities": aggregated_discrete_probabilities_success,
                    "cumulative_probabilities": aggregated_cumulative_probabilities_success,
                },
                "fails": {
                    "full_range": aggregated_full_range,
                    "discrete_probabilities": aggregated_discrete_probabilities_fails,
                    "cumulative_probabilities": aggregated_cumulative_probabilities_fails,
                }
            }
        else:
            simulation_results = self.simulate_dice_rolls(total_number_of_dice, target, **reroll_params)
        return simulation_results

    def simulate_rolls_for_wounds(self, data):
        mode = data.encounter_params['action_type']
        
        if mode == "Clash":
            defense_results = self.simulate_rolls_by_type(data, "defense")
            morale_results = self.simulate_rolls_by_type(data, "morale")
            
            aggregated_discrete_probabilities = defense_results["fails"]["discrete_probabilities"] + morale_results["fails"]["discrete_probabilities"]
            aggregated_cumulative_probabilities = np.cumsum(aggregated_discrete_probabilities[::-1])[::-1]
            aggregated_full_range = defense_results["fails"]["full_range"]
            
            return {
                "discrete_probabilities": aggregated_discrete_probabilities,
                "cumulative_probabilities": aggregated_cumulative_probabilities,
                "full_range": aggregated_full_range
            }
        
        elif mode == "Volley":
            defense_results = self.simulate_rolls_by_type(data, "defense")
            
            aggregated_discrete_probabilities = defense_results["fails"]["discrete_probabilities"]
            aggregated_cumulative_probabilities = np.cumsum(aggregated_discrete_probabilities[::-1])[::-1]
            aggregated_full_range = defense_results["fails"]["full_range"]
            
            return {
                "discrete_probabilities": aggregated_discrete_probabilities,
                "cumulative_probabilities": aggregated_cumulative_probabilities,
                "full_range": aggregated_full_range
            }
        
        else:
            raise ValueError("Invalid mode. Only 'Clash' and 'Volley' modes are supported.")

    def simulate_killed_stands(self):
        pass
