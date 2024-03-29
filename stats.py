import numpy as np

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
                discrete_probabilities_full[value - 1] = prob

        # Calculate cumulative probabilities
        cumulative_probabilities_full = np.cumsum(discrete_probabilities_full[::-1])[::-1]

        return discrete_probabilities_full, cumulative_probabilities_full, full_range


