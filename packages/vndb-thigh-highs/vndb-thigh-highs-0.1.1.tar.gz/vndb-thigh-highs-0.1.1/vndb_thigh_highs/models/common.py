from enum import Enum

class SpoilerLevel(Enum):
    NOT_A_SPOILER = 0
    MINOR_SPOILER = 1
    SPOILER = 2

class Gender(Enum):
    FEMALE = 'f'
    MALE = 'm'
    BOTH = 'b'
