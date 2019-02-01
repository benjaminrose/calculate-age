import numpy as np

import calculate_age

print('ok')
print(calculate_age.__version__)

# test ramp
############
print('test ramp')
print(calculate_age.ramp(5))
print(calculate_age.ramp(50))
print(calculate_age.ramp(0))
print(calculate_age.ramp(-1))
# can I make it work as a vector?
# print(calculate_age.ramp(np.arange(5)))


# four_param_tau
#################
print('\ntest four_param_tau')
print(calculate_age.four_param_tau(1, 0.1, 3, 1))
print(calculate_age.four_param_tau(1.2, 0.1, 3, 1)) # should be less

print(calculate_age.four_param_tau(3.5, 0.1, 3, 1))
print(calculate_age.four_param_tau(3.8, 0.1, 3, 1)) # should be more
# test a time vector
# print(calculate_age.four_param_tau(np.array([1, 2, 3, 4]), 0.1, 3, 1))


def sf_trans_to_sf_percent(sf_trans_since_BB, sf_start_t, age_of_universe):
    """Takes a sf_trans_since_BB and translates it to a percentage."""
    return (sf_trans_since_BB - sf_start_t)/(age_of_universe - sf_start_t)

# test age
###########
print('\ntest ages')
# Does it run?
# print(calculate_age.age(0.1, 1, 0.75, 0.5, 0.1))

# Does it run correctly?
# to test with table 5 data, age(z=0.05) = 13.1917132 Gyr
# sf_trans_percent = (sf_trans_since_BB - sf_start_t)/(age_of_universe - sf_start_t)
print(calculate_age.age(0.5, 1.5, 0.6697, -0.785, 0.05))
print(calculate_age.age(0.5, 1.5, sf_trans_to_sf_percent(9.0, 1.5, 13.1917132), -0.785, 0.05))
print(calculate_age.age(0.5, 1.5, 0.6697, 1.504, 0.05))
print(calculate_age.age(0.1, 8.0, 0.7705, 1.52, 0.05))

# can it take arrays
# print(calculate_age.age([0.1, 0.1], [1, 1], [0.75, 0.75], [0.5, 0.5], 0.1))