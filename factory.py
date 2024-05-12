from building import Building
from floor import Floor
from elevator import Elevator

def factory(object_type, *args, **kwargs):
    type_dict = {
        "building": Building,
        "floor": Floor,
        "elevator": Elevator
    }
    return type_dict[object_type](*args, **kwargs) if object_type in type_dict else None
