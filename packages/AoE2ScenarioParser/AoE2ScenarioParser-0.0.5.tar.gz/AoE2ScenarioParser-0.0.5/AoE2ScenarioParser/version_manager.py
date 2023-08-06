from enum import Enum


class Change(Enum):
    REMOVED = -1
    ADDED = 1
    DATATYPE_CHANGE = 2
    NAME_CHANGE = 3


version_changes = {
    "MapPiece": {
        "Villager Force Drop": {
            ">=1.37": Change.ADDED
        }
    }
}


def validate_version(file_version, version_string):
    """
        '>x': Change after
        '>=x': Change from
        'x-x': Change between
        '<x': Change until
        '<=x': Change until with
    """
    pass


validate_version("1.37", "<1.37")
