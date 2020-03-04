"""
Pretifies table, and changes False -> No terminado
                             True  -> Terminado

"""


def pretify_done(b: bool) -> str:
    return 'Terminado' if b else 'No terminado'
