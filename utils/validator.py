
def contains_value(a, b, c):

    for stuff in b:
        if stuff.get(c) == a:

            return True
    return False


def has_role(to_check, roles, _id=None):

    if _id is not None:

        for rol in roles:
            if rol.id == to_check:
                return True
        return False
    else:
        for rol in roles:
            if rol.name == to_check:
                return True
        return False
