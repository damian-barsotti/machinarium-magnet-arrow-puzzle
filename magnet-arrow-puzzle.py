# This code models the Magnet Arrow Puzzle from the game Machinarium.
#
# https://amanita-design.net/games/machinarium.html
#
# Another solution in https://gist.github.com/antazoey/e70e9751227ef96c0c42df3a158949d8
# That is by brute force and with fixed amount of arrows

from dataclasses import dataclass
from enum import Enum
from typing import List

class Arrow(Enum):
    """The different arrows.
    The arrows can be  UP or DOWN
    """
    DOWN = 0
    UP = 1

    def __str__(self):
        match self.value:
            case 0:
                return '>'
            case 1:
                return '<'


class Panel:
    """ Panel is represented by two list of arrows,
    one for the arrows above de hole and another for arrows below
    """

    def __init__(self, num_arrow = 3):

        
        self.above: List[Arrow] = [Arrow.DOWN] * num_arrow
        self.below: List[Arrow] = [Arrow.UP] * num_arrow

        self.num_arrow = num_arrow

        self.num_move = 0

    def __str__(self):
        return ' '.join(map(str, self.above + [0] + list(reversed(self.below))))

    def move_arrow_up(self):

        a = self.below.pop()

        assert a == Arrow.UP

        self.above.append(a)

        self.num_move += 1

        print(self)

        return self

    def move_arrow_down(self):
        
        a = self.above.pop()

        assert a == Arrow.DOWN

        self.below.append(a)

        self.num_move += 1
        
        print(self)

        return self

    def move_arrow_skip_up(self):

        ad = self.below.pop()
        assert ad == Arrow.DOWN

        au = self.below.pop()
        assert au == Arrow.UP

        self.above.append(au)
        self.above.append(ad)

        self.num_move += 1
        
        print(self)

        return self

    def move_arrow_skip_down(self):

        au = self.above.pop()
        assert au == Arrow.UP

        ad = self.above.pop()
        assert ad == Arrow.DOWN

        self.below.append(ad)
        self.below.append(au)

        self.num_move += 1
        
        print(self)

        return self

def even(n: int) -> bool:
    return n % 2 == 0

def oppositor(p: Panel)-> Panel:

    n = p.num_arrow

    if n == 0:
        return p

    if n == 1: # Base case
        p.move_arrow_up()
        return p

    # n > 1

    # recursive call
    p.num_arrow = n-1
    p = oppositor(p)
    p.num_arrow = n

    if even(n-1): # opposites are below

        for _ in range(n-1):
            p.move_arrow_skip_up()

        p.move_arrow_up()

    else: # odd(n) opposites are above

        for _ in range(n-1):
            p.move_arrow_skip_down()

        p.move_arrow_down()

    return p

def mover(p: Panel) -> Panel:

    n = p.num_arrow

    if n == 0:
        return p

    if n == 1: # Base case
        # Opposites are above
        p.move_arrow_skip_down()
        p.move_arrow_up()
        return p
    
    # n > 1

    if even(n):  # opposites are below

        for _ in range(n):
            p.move_arrow_skip_up()

        p.move_arrow_down()

    else:  # odd(n) opposites are above

        for _ in range(n):
            p.move_arrow_skip_down()

        p.move_arrow_up()

    # recursive call
    p.num_arrow = n-1
    p = mover(p)
    p.num_arrow = n

    return p

if __name__ == "__main__":

    num_arrow = None

    while num_arrow is None:
        try:
            num_arrow = int(input("Please enter the number of arrows: "))
            if num_arrow < 0:
                print("Number of arrow must be non negative")
                num_arrow = None
                
        except ValueError:
            print("Invalid integer!")

    p = Panel(num_arrow)
    print(p)
    p = mover(oppositor(p))

    print(f"Number of moves: {p.num_move}")