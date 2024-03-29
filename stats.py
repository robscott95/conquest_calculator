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
        
        # Perform rerolls where criteria are met and ensure each die is only rerolled once
        reroll_indices = np.where(need_reroll)
        new_rolls = np.random.randint(1, 7, reroll_indices[0].shape)
        rolls[reroll_indices] = new_rolls

        # Recalculate success counts after rerolls
        success_counts = np.sum(rolls <= target, axis=1)

        unique, counts = np.unique(success_counts, return_counts=True)
        discrete_probabilities = counts / simulations

        full_range = np.arange(0, total_number_of_dice+1)
        discrete_probabilities_full = np.zeros(total_number_of_dice + 1)
        cumulative_probabilities_full = np.zeros(total_number_of_dice + 1)

        # Fill in the probabilities
        for value, prob in zip(unique, discrete_probabilities):
            if 0 <= value <= total_number_of_dice:
                discrete_probabilities_full[value] = prob

        # Calculate cumulative probabilities
        cumulative_probabilities_full = np.cumsum(discrete_probabilities_full[::-1])[::-1]

        return {
            "success_counts": success_counts,
            "fail_counts": np.clip(total_number_of_dice - success_counts, a_min=0, a_max=None),
            "full_range": full_range,
            "unique": unique,
            "discrete_probabilities": discrete_probabilities_full, 
            "cumulative_probabilities": cumulative_probabilities_full, 
        }
    
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
            max_full_range = max(previous_simulation_results["full_range"])
            
            aggregated_discrete_probabilities = np.zeros(max_full_range + 1)
            aggregated_cumulative_probabilities = np.zeros(max_full_range + 1)
            aggregated_killed_stands_discrete_probabilities = np.zeros(max_full_range + 1)
            average_fail_counts = 0
            average_killed_stands_count = 0
            
             # Aggregate results based on the distribution of previous phase outcomes
            for outcome, probability in zip(previous_simulation_results["full_range"], previous_simulation_results["discrete_probabilities"]):
                if probability > 0:  # Only simulate for outcomes that occurred
                    current_results = self.simulate_dice_rolls(
                        outcome, target, simulations=10000, **reroll_params  # Simulate based on the outcome as total dice
                    )

                    max_full_range = max(max_full_range, max(current_results['full_range']))
                    # The simulation returns a dictionary; extract discrete probabilities
                    discrete_probabilities = np.zeros(max_full_range + 1)
                    discrete_probabilities[:len(current_results["discrete_probabilities"])] = current_results["discrete_probabilities"]
                    
                    # Weight discrete probabilities by the probability of the outcome occurring
                    weighted_discrete_probabilities = discrete_probabilities * probability
                    
                    # Aggregate weighted probabilities into the total distribution
                    # This assumes the length of weighted_discrete_probabilities aligns with aggregated results arrays
                    aggregated_discrete_probabilities += weighted_discrete_probabilities


                    # Add data related to killed stands
                    average_fail_counts = average_fail_counts + np.mean(current_results["fail_counts"] * probability)
                    killed_stands = current_results["fail_counts"] / data.target_input_wounds_per_stand
                    killed_stands = np.floor(killed_stands)
                    unique, counts = np.unique(killed_stands, return_counts=True)
                    killed_stands_discrete_probabilities = counts / 10000
                    weighted_killed_stands_discrete_probabilities = killed_stands_discrete_probabilities * probability
                    aggregated_killed_stands_discrete_probabilities += weighted_killed_stands_discrete_probabilities
                    print(unique, counts)

            aggregated_cumulative_probabilities = np.cumsum(aggregated_discrete_probabilities[::-1])[::-1]
            aggregated_full_range = np.arange(0, max_full_range+1)
            simulation_results = {
                "full_range": aggregated_full_range,
                "fail_counts": average_fail_counts,
                "discrete_probabilities": aggregated_discrete_probabilities, 
                "cumulative_probabilities": aggregated_cumulative_probabilities, 
                "killed_stands_discrete_probabilities": aggregated_killed_stands_discrete_probabilities,
            }
        else:
            simulation_results = self.simulate_dice_rolls(total_number_of_dice, target, **reroll_params)
        return simulation_results
