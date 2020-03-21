def has_role(roles, role, by_id= False):
    if by_id:
        for rol in roles:
            if rol.id == role:
                return True
        return False
    else:
        for rol in roles:
            if rol.name == role:
                return True
        return False


def has_permissions(id: int, action_id: int):
    raise Exception('Not yet implemented')


"""
1: Puede hacer todo
2:
3:
4:
5:

"""
# TODO crear tabla con todos los usuarios/ids para poder
