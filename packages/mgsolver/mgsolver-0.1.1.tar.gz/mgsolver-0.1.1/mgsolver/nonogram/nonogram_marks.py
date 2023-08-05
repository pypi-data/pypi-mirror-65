class NonogramMarks:
    X = 'X'
    O = 'O'
    N = ' '


def value_to_mark(value: int) -> str:
    return NonogramMarks.N if value == 0 else NonogramMarks.O if value > 0 else NonogramMarks.X
