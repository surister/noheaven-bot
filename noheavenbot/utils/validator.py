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


def has_permissions(id: int, action_id: int):
    pass


"""
1: Puede hacer todo
2:
3:
4:
5:

"""

# TODO crear tabla con todos los usuarios/ids para poder
