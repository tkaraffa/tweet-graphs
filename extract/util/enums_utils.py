from enum import Enum


def join_enums(enum: Enum):
    return ",".join([entry.value for entry in enum])


def dictify_enums(enum: Enum):
    return {entry.name.lower(): entry.value.lower() for entry in enum}
