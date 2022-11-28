class ValidateHelper():
    """ A static class that validates information before querying or
        being sent to the database.
    """

    @staticmethod
    def validate_not_none(obj) -> bool:
        if obj is None or type(obj) is None:
            raise TypeError(f'{obj} cannot be {None}')
        return True

    @staticmethod
    def validate_obj_is_of_type(obj, *, desired_type) -> bool:
        if type(obj) is not desired_type:
            raise TypeError(f'{obj} must be of type {desired_type}')
        return True

    @staticmethod
    def validate_num_is_pos(num: int) -> bool:
        if num < 0:
            raise ValueError(f'{num} must be positive')
        return True

    @staticmethod
    def validate_id_is_int_and_pos(id: int) -> bool:
        ValidateHelperSingleton.validate_obj_is_of_type(id, desired_type=int)
        ValidateHelperSingleton.validate_num_is_pos(id)
        return True

class DebugHelper():
    """ A static class that helps print useful information for debugging.
        NOTE: Can be removed before production.
    """

    @staticmethod
    def print_objs(arg_names, *args):
        for arg_name, arg_val in zip(arg_names, args):
            print(f'\t{arg_name}={arg_val}')


ValidateHelperSingleton = ValidateHelper()
DebugHelperSingleton = DebugHelper()