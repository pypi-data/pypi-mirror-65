from copy import deepcopy


def dict_inject(initial_dict, values, _keys_=None):
    """
    This utility perform an operation similar to initial_dict.
    """
    result_dict = deepcopy(initial_dict)

    for key, value in values.items():
        if key in result_dict:
            # We save the key name recursively for error display in case of Exception
            if _keys_ is None:
                subkeys = key
            else:
                subkeys = _keys_ + '.' + key

            if isinstance(value, dict):
                # We need to recursively apply dict_inject
                result_dict[key] = dict_inject(result_dict[key], value, subkeys)
            elif result_dict[key] != value:
                raise Exception("Conflicting values for {}: current value is '{}', trying to update to '{}'".format(subkeys, result_dict[key], value))
        else:
            # Key does not exist: we set it.
            result_dict[key] = value
    return result_dict

