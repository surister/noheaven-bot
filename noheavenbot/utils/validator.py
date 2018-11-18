
def contains_value(a, b, c):

    for stuff in b:
        return stuff.get(c) == a
    return False


def has_role(to_check, roles, _id=None):

    if _id is not None:

        for rol in roles:
            return rol.id == to_check

        return False
    else:
        for rol in roles:
            return rol.name == to_check
        return False
