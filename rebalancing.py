import sys

import numpy as np

wanted_distribution = np.array([60, 25, 5, 5, 5]) / 100  # Wished portfolio distribution in percent.
current_holdings = np.array([937, 486, 122, 122, 69])  # current total amount of holdings
savings_amount = 600


def checks():
    if wanted_distribution.sum() != 1:
        sys.exit("Portfolio holdings do not add up to 100%.")
    if len(wanted_distribution) != len(current_holdings):
        sys.exit("Wanted distribution needs to have same amount of holdings as current holdings")


def calculate_distributed_saving_amount():
    global new_distribution
    total_savings = current_holdings.sum()
    current_distribution = (current_holdings / total_savings)
    relative_imbalances = 1 - (current_distribution / wanted_distribution)

    new_distribution_basis_index = relative_imbalances.argmin()

    new_distribution_basis = current_holdings[new_distribution_basis_index] / (
                wanted_distribution[new_distribution_basis_index] * 100)
    target_holdings = np.around(new_distribution_basis * wanted_distribution * 100)

    missing_for_full_rebalance = target_holdings - current_holdings
    min_full_rebalance_amount = round(missing_for_full_rebalance.sum())
    print(f'min amount for full rebalance: {min_full_rebalance_amount}')
    print(f'provided savings amount: {savings_amount}')

    savings_amount_remaining = savings_amount
    new_holdings = current_holdings
    max_iterations = 1000
    while savings_amount_remaining > 0:
        missing_for_full_rebalance = target_holdings - new_holdings
        relative_missing = np.around(missing_for_full_rebalance / target_holdings, 3)
        new_distribution = new_holdings / new_holdings.sum()
        new_holdings, savings_amount_remaining = calculate_rebalancing_step(savings_amount_remaining, target_holdings,
                                                                            relative_missing,
                                                                            missing_for_full_rebalance, new_holdings)
        print(f'savings amount remaining: {savings_amount_remaining}')
        print(f'currently new holdings: {new_holdings}')
        print(f'currently new distribution: {new_distribution}')
        if max_iterations < 0:
            sys.exit("CALCULATION INTERRUPTED DUE TO INF LOOP")
        max_iterations -= 1
    print('\n--------------------------------- done with calculation ---------------------------------------------')
    print(f'total used savings-amount: {np.sum(np.around(new_holdings)) - np.around(current_holdings).sum()}')
    print(f'final distribution: {np.around(new_distribution, 2)}')
    print('\n---------------------------------     amounts to add    ---------------------------------------------')
    total = 0
    for i, val in enumerate(new_distribution):
        amount_to_add = round(new_holdings[i]) - round(current_holdings[i])
        print(f'Holding {i+1}: Add {amount_to_add}')
        total += amount_to_add
    print(f'--------------------------')
    print(f'in total: {total}')
    return new_holdings


def calculate_rebalancing_step(savings_amount_remaining, target_holdings, relative_missing, missing_for_full_rebalance,
                               current_holdings):
    first_max_relative_index = np.argmax(relative_missing)
    max_relative_indices = [i for i, val in enumerate(relative_missing) if val == relative_missing[
        first_max_relative_index]]  # Indices of holdings that need to be increased to target
    target_index = np.argmax(relative_missing < relative_missing[first_max_relative_index])
    percentage_diff_to_next_bigger = relative_missing[first_max_relative_index] - relative_missing[target_index]

    required_savings_amount = percentage_diff_to_next_bigger * target_holdings[max_relative_indices].sum()

    if required_savings_amount > savings_amount_remaining:
        max_possible_target_percentage = relative_missing[first_max_relative_index] - savings_amount_remaining / \
                                         target_holdings[max_relative_indices].sum()
        max_possible_percentage_raise = relative_missing[first_max_relative_index] - max_possible_target_percentage
        amount_to_add = [val * max_possible_percentage_raise if index in max_relative_indices else 0 for index, val in
                         enumerate(target_holdings)]
    else:
        if required_savings_amount != 0:
            amount_to_add = [val * percentage_diff_to_next_bigger if index in max_relative_indices else 0 for index, val in enumerate(target_holdings)]
        else:
            amount_to_add = wanted_distribution * savings_amount_remaining

    savings_amount_remaining -= round(np.sum(amount_to_add))
    print(f'used savings amount: {round(np.sum(amount_to_add))}')

    new_distribution = np.add(current_holdings, amount_to_add)
    return new_distribution, savings_amount_remaining


if __name__ == '__main__':
    checks()
    savings_distributed = calculate_distributed_saving_amount()
