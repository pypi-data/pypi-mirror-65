def _compute_string(*args, reverse=False):
    """
        Compute only string
        Return computed string
    """
    # Tmp value
    res = ""
    # Loop over args
    for arg in args:
        res += arg
    # Return
    # If reverse
    if reverse:
        return res[::-1]
    return res


def _compute_number(*args):
    """
        Compute only number
        Return computed number
    """
    # Tmp value
    res = 0
    # Loop over args
    for arg in args:
        res += arg
    # Return
    return res


def _checktype(*args):
    """
        Return type of args
        The first type arg define for each other
        If multiple type, raise Error
    """
    # Loop over args
    res = None
    for arg in args:
        # If not previous value
        if res is None:
            res = type(arg)
        else:
            # Raise if error
            if type(arg) != res:
                raise ValueError("Mixing {0} and {1} type !".format(type(arg), res))
    return res


def compute(*args, reverse=False):
    """
        Compute any  params
        Return computed
    """
    # Check type of each
    type_of_args = _checktype(*args)
    #  For each type ...
    if type_of_args == str:
        return _compute_string(*args, reverse=reverse)
    elif type_of_args == int:
        return _compute_number(*args)
