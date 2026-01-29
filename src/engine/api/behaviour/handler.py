from engine.api.behaviour.structs import BehaviourHandler

store: dict[int, BehaviourHandler] = {}


def command(index: int):
    def decorator(func: BehaviourHandler) -> BehaviourHandler:
        store[index] = func
        return func

    return decorator
