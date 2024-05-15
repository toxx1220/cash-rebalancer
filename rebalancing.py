import sys

import numpy as np

wanted_distribution = np.array({60, 25, 5, 5, 5})  # Wished Portfolio distribution in Percent.
current_holdings = np.array({1000, 360, 110, 100, 100})  # current total amount of holdings
savings_amount = 160


def checks():
    if wanted_distribution.sum() != 100 \
            or len(wanted_distribution) != len(current_holdings):
        sys.exit("Portfolio holdings do not add up to 100%.")


def calculate_distributed_saving_amount():
    total_savings = current_holdings.sum()
    current_distribution = (current_holdings / total_savings) * 100  # 1 Percent = 1.
    disbalances = wanted_distribution - current_distribution
    relative_disbalances = current_distribution / wanted_distribution

    new_distribution_basis_index = relative_disbalances.argmin()
    new_distribution_basis = current_holdings[new_distribution_basis_index] / current_distribution[
        new_distribution_basis_index]
    target_distribution = new_distribution_basis * wanted_distribution

    missing_for_full_rebalance = target_distribution - current_distribution
    min_full_rebalance_amount = missing_for_full_rebalance.sum()
    print(f'min amount for full rebalance: {min_full_rebalance_amount}')

    relative_missing = missing_for_full_rebalance / target_distribution

    savings_amount_remaining = savings_amount
    new_distribution = current_distribution
    while savings_amount_remaining > 0:
        savings_amount_remaining = calculate_rebalancing_step(savings_amount_remaining, relative_missing, missing_for_full_rebalance, current_distribution, new_distribution)


def calculate_rebalancing_step(savings_amount_remaining, relative_missing, missing_for_full_rebalance, current_distribution, new_distribution):

    first_min_relative_index = np.argmin(relative_missing)
    min_relative_indices = [i for val, i in relative_missing if val == relative_missing[first_min_relative_index]]  # Indices of holdings that need to be increased to target
    target_index = np.argmin(relative_missing > relative_missing[first_min_relative_index])
    percentage_diff_to_next_bigger = relative_missing[first_min_relative_index] - relative_missing[target_index]

    required_savings_amount = percentage_diff_to_next_bigger * current_distribution[min_relative_indices].sum()

    if required_savings_amount > savings_amount_remaining:
        max_possible_percentage_raise = relative_missing[target_index] - savings_amount_remaining / current_distribution[min_relative_indices].sum()
        new_distribution = np.add(current_distribution, )




    return 0


if __name__ == '__main__':
    checks()
    savings_distributed = calculate_distributed_saving_amount()
