import numpy as np
from numbers import *


def n_conditions_to_combinations(
        n_conditions,
        axis_combinations=0,
        n_repetitions_combinations=1,
        order_variables='rl',
        variables_in_order=None,
        dtype=int):

    # order_variables is the order of the variables by which they change their own conditions.
    # order_variables can either be 'rl' for right-to-left, 'lr' for left-to-right or 'c' for custom.
    # If order_variables=='c', then variables_in_order must be a list, a tuple or an 1-d array containing the variables
    # in the custom order by which the variables change their own conditions:
    #
    # Requirements:
    # 1) order_variables == 'rl' or order_variables == 'lr' or order_variables == 'c';
    # If order_variables=='c', then:
    #     2) len(variables_in_order) == len(n_conditions);
    #     3) variables_in_order must contain all integers from 0 to (len(n_conditions)-1);
    #     4) variables_in_order cannot contain repeated integers.

    n_variables = len(n_conditions)
    if n_variables > 0:
        from ccalafiore.array import pad_array_from_n_samples_target
        variables = np.arange(n_variables)
        # n_conditions = np.asarray(n_conditions, dtype=int)
        # conditions = n_conditions_to_conditions(n_conditions)
        n_combinations = np.prod(n_conditions) * n_repetitions_combinations
        if n_combinations < 0:
            n_conditions = n_conditions.astype(np.int64)
            n_combinations = np.prod(n_conditions) * n_repetitions_combinations

        # axis_combinations = int(not(bool(axis_variables)))
        axis_variables = int(not(bool(axis_combinations)))
        shape_combinations = np.empty(2, dtype=int)
        shape_combinations[axis_combinations] = n_combinations
        shape_combinations[axis_variables] = n_variables

        combinations = np.empty(shape_combinations, dtype=dtype)

        if order_variables == 'rl':
            variables_in_order = variables[::-1]
        elif order_variables == 'lr':
            variables_in_order = variables
        elif order_variables == 'c':
            variables_in_order = np.asarray(variables_in_order, dtype=int)
            # check requirement 2
            if len(variables_in_order) != n_variables:
                raise ValueError('The following condition must be met:\nlen(variables_in_order) == len(n_conditions).')
            # check requirement 3
            for v in range(n_variables):
                if v not in variables_in_order:
                    raise ValueError('variables_in_order must contain all integers from 0 to (len(n_conditions)-1).\n'
                                     '{} is not in variables_in_order.'.format(v))
            # check requirement 4
            for v in variables_in_order:
                if np.sum(v == variables_in_order) > 1:
                    raise ValueError('variables_in_order cannot contain repeated integers.\n'
                                     '{} is a repeated integer.'.format(v))
        else:
            # check requirement 1
            raise ValueError(
                'order_variables can either be \'rl\' for right-to-left, '
                '\'lr\' for left-to-right or \'c\' for custom.\n'
                'Now, order_variables = {}'.format(order_variables))

        i_variable = variables_in_order[0]
        indexes_combinations = np.empty(2, dtype=object)
        indexes_combinations[axis_variables] = i_variable
        for i_condition in range(n_conditions[i_variable]):
            indexes_combinations[axis_combinations] = slice(i_condition, n_combinations, n_conditions[i_variable])
            combinations[tuple(indexes_combinations)] = i_condition

        indexes_combinations[axis_combinations] = slice(None)

        # combinations[tuple(indexes_combinations)] = np.expand_dims(
        #     pad_array_from_n_samples_target(conditions[-1], n_samples_target=n_combinations),
        #     axis=axis_variables)
        cumulative_n_combinations = n_conditions[i_variable]
        for i_variable in variables_in_order[1:]:
            cumulative_combinations = np.empty(
                cumulative_n_combinations * n_conditions[i_variable], combinations.dtype)
            for i_condition in range(n_conditions[i_variable]):
                cumulative_combinations[
                    slice(i_condition * cumulative_n_combinations,
                          (i_condition + 1) * cumulative_n_combinations)] = i_condition

            indexes_combinations[axis_variables] = i_variable
            if cumulative_combinations.size < n_combinations:
                combinations[tuple(indexes_combinations)] = pad_array_from_n_samples_target(
                    cumulative_combinations, n_samples_target=n_combinations)
            elif cumulative_combinations.size == n_combinations:
                combinations[tuple(indexes_combinations)] = cumulative_combinations
            else:
                raise Exception('something wrong')
            cumulative_n_combinations *= n_conditions[i_variable]

        # if change_dtype:
        #     combinations = combinations.astype(dtype_end)
    else:
        combinations = []
    return combinations


def conditions_to_combinations(
        conditions,
        axis_combinations=0,
        n_repetitions_combinations=1,
        order_variables='rl',
        variables_in_order=None,
        dtype=None):

    # order_variables is the order of the variables by which they change their own conditions.
    # order_variables can either be 'rl' for right-to-left, 'lr' for left-to-right or 'c' for custom.
    # If order_variables=='c', then variables_in_order must be a list, a tuple or an 1-d array containing the variables
    # in the custom order by which the variables change their own conditions:
    #
    # Requirements:
    # 1) order_variables == 'rl' or order_variables == 'lr' or order_variables == 'c';
    # If order_variables=='c', then:
    #     2) len(variables_in_order) == len(conditions);
    #     3) variables_in_order contains all integers from 0 to (len(conditions)-1);
    #     4) variables_in_order cannot contain repeated integers.

    n_variables = len(conditions)
    if n_variables > 0:
        from ccalafiore.array import pad_array_from_n_samples_target
        variables = np.arange(n_variables)
        # conditions = np.asarray(conditions, dtype=object)
        n_conditions = conditions_to_n_conditions(conditions)
        n_combinations = np.prod(n_conditions) * n_repetitions_combinations
        if n_combinations < 0:
            n_conditions = n_conditions.astype(np.int64)
            n_combinations = np.prod(n_conditions) * n_repetitions_combinations

        if dtype is None:
            dtype = type(conditions[0][0])

        change_dtype = False
        if dtype == str:
            dtype_end = str
            dtype = object
            change_dtype = True

        axis_variables = int(not(bool(axis_combinations)))
        shape_combinations = np.empty(2, dtype=int)
        shape_combinations[axis_combinations] = n_combinations
        shape_combinations[axis_variables] = n_variables

        combinations = np.empty(shape_combinations, dtype=dtype)

        if order_variables == 'rl':
            variables_in_order = variables[::-1]
        elif order_variables == 'lr':
            variables_in_order = variables
        elif order_variables == 'c':
            variables_in_order = np.asarray(variables_in_order, dtype=int)
            # check requirement 2
            if len(variables_in_order) != n_variables:
                raise ValueError('The following condition must be met:\nlen(variables_in_order) == len(conditions).')
            # check requirement 3
            for v in range(n_variables):
                if v not in variables_in_order:
                    raise ValueError('variables_in_order must contain all integers from 0 to (len(conditions)-1).\n'
                                     '{} is not in variables_in_order.'.format(v))
            # check requirement 4
            for v in variables_in_order:
                if np.sum(v == variables_in_order) > 1:
                    raise ValueError('variables_in_order cannot contain repeated integers.\n'
                                     '{} is a repeated integer.'.format(v))
        else:
            # check requirement 1
            raise ValueError(
                'order_variables can either be \'rl\' for right-to-left, '
                '\'lr\' for left-to-right or \'c\' for custom.\n'
                'Now, order_variables = {}'.format(order_variables))

        i_variable = variables_in_order[0]
        indexes_combinations = np.empty(2, dtype=object)
        indexes_combinations[axis_variables] = i_variable
        for i_condition in range(n_conditions[i_variable]):
            indexes_combinations[axis_combinations] = slice(i_condition, n_combinations, n_conditions[i_variable])
            combinations[tuple(indexes_combinations)] = conditions[i_variable][i_condition]

        indexes_combinations[axis_combinations] = slice(None)

        # combinations[tuple(indexes_combinations)] = np.expand_dims(
        #     pad_array_from_n_samples_target(conditions[-1], n_samples_target=n_combinations),
        #     axis=axis_variables)
        cumulative_n_combinations = n_conditions[i_variable]
        for i_variable in variables_in_order[1:]:
            cumulative_combinations = np.empty(
                cumulative_n_combinations * n_conditions[i_variable], combinations.dtype)
            for i_condition in range(n_conditions[i_variable]):
                cumulative_combinations[
                    slice(i_condition * cumulative_n_combinations,
                          (i_condition + 1) * cumulative_n_combinations)] = conditions[i_variable][i_condition]

            indexes_combinations[axis_variables] = i_variable
            if cumulative_combinations.size < n_combinations:
                combinations[tuple(indexes_combinations)] = pad_array_from_n_samples_target(
                    cumulative_combinations, n_samples_target=n_combinations)
            elif cumulative_combinations.size == n_combinations:
                combinations[tuple(indexes_combinations)] = cumulative_combinations
            else:
                raise Exception('something wrong')
            cumulative_n_combinations *= n_conditions[i_variable]

        if change_dtype:
            combinations = combinations.astype(dtype_end)
    else:
        combinations = []
    return combinations


def make_combinations_of_conditions_as_distributions(conditions_as_distributions, n_repetitions_combinations=1):

    n_variables = len(conditions_as_distributions)
    n_conditions = np.empty(n_variables, dtype=object)

    for i_variable in range(n_variables):

        n_conditions[i_variable] = len(conditions_as_distributions[i_variable])

    combinations_of_conditions = n_conditions_to_combinations(n_conditions)

    n_combinations = len(combinations_of_conditions)

    combinations_of_conditions_as_distributions = np.empty([n_combinations, n_variables], dtype=int)

    for i_variable in range(n_variables):

        for i_condition in range(n_conditions[i_variable]):

            indexes_of_i_condition = np.argwhere(combinations_of_conditions[:, i_variable] == i_condition)

            n_i_condition = len(indexes_of_i_condition)

            combinations_of_conditions_as_distributions[indexes_of_i_condition, i_variable] = \
                np.random.choice(conditions_as_distributions[i_variable][i_condition],
                                 n_i_condition)[:, None]

    return combinations_of_conditions_as_distributions


def trials_to_combinations(
        trials, axis_combinations=0, variables=None,  n_repetitions_combinations=1, dtype=None):

    conditions = trials_to_conditions(trials, axis_combinations=axis_combinations, variables=variables)
    combinations = conditions_to_combinations(
        conditions,
        axis_combinations=axis_combinations,
        n_repetitions_combinations=n_repetitions_combinations,
        dtype=dtype)
    return combinations


def trials_to_conditions(trials, axis_combinations=0, variables=None):

    from ccalafiore.array import advanced_indexing

    axis_variables = int(not(bool(axis_combinations)))
    if variables is None:
        n_variables = trials.shape[axis_variables]
        variables = np.arange(n_variables)
    else:
        try:
            n_variables = len(variables)
        except TypeError:
            variables = np.asarray([variables], dtype=int)
            n_variables = len(variables)

    conditions = np.empty(n_variables, dtype=object)

    indexes_trials_adv = np.empty(2, dtype=object)
    indexes_trials_adv[axis_combinations] = np.arange(trials.shape[axis_combinations])

    indexes_trials_slice = np.full(2, 0, dtype=object)
    indexes_trials_slice[axis_combinations] = slice(None)
    indexes_trials_slice = tuple(indexes_trials_slice)

    for i_variable in range(n_variables):

        indexes_trials_adv[axis_variables] = variables[i_variable]
        trials_variables_i = trials[advanced_indexing(indexes_trials_adv)]
        trials_variables_i = trials_variables_i[indexes_trials_slice]

        conditions[i_variable] = np.unique(trials_variables_i)

    return conditions


def trials_to_n_conditions(trials, axis_combinations=0, variables=None):
    conditions = trials_to_conditions(trials, axis_combinations=axis_combinations, variables=variables)
    n_conditions = conditions_to_n_conditions(conditions)
    # n_variables = len(conditions)
    # n_conditions = np.empty(n_variables, dtype=int)
    # for i_variable in range(n_variables):
    #     n_conditions[i_variable] = len(conditions[i_variable])
    return n_conditions


def n_conditions_to_conditions(n_conditions):
    n_variables = len(n_conditions)
    conditions = np.empty(n_variables, dtype=object)
    for i_variable in range(n_variables):
        conditions[i_variable] = np.arange(n_conditions[i_variable])
    return conditions


def conditions_to_n_conditions(conditions):
    n_variables = len(conditions)
    n_conditions = np.empty(n_variables, dtype=int)
    for i_variable in range(n_variables):
        n_conditions[i_variable] = len(conditions[i_variable])
    return n_conditions
