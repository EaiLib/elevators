from building import Building
from floor import Floor
from elevator import Elevator

def factory(object_type: str, *args, **kwargs):
    """
    Factory function to create instances of Building, Floor, or Elevator objects.

    This function creates instances of Building, Floor, or Elevator objects based on the
    provided object type. It returns None if the object type is not recognized.

    Parameters:
        object_type (str): The type of object to create.
        *args: Variable length argument list passed to the object constructor.
        **kwargs: Arbitrary keyword arguments passed to the object constructor.

    Returns:
        object: An instance of the specified object type, or None if the object type
            is not recognized.
    """
    type_dict = {
        "building": Building,
        "floor": Floor,
        "elevator": Elevator
    }
    return type_dict[object_type](*args, **kwargs) if object_type in type_dict else None
