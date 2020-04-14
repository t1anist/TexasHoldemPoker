from enum import Enum


class boardTexture(Enum):
    No_Salient = 0
    Flush_Possible = 1
    Straight_Possible = 2
    Flush_Possible_Straight_Possible = 3
    Straight_High_Possible = 4
    Flush__Possible_Straight_High_Possible = 5
    Flush_High_Possible = 6
    Flush_High_Possible_Straight_Possible = 7
    Flush_High_Possible_Straight_High_Possible = 8


