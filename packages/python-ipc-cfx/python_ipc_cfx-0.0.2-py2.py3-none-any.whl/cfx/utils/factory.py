from ..Production.TestAndInspection import UnitsInspected

ALL_OBJECTS = {
    "UnitsInspected": UnitsInspected
}


def create_object(class_name, data):
    return ALL_OBJECTS[class_name](data)
