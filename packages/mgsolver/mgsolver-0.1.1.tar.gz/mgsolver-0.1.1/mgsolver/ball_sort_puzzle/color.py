class Color:
    blue = 0
    brown = 1
    darkgreen = 2
    gray = 3
    green = 4
    lightblue = 5
    lightgreen = 6
    orange = 7
    pink = 8
    purple = 9
    red = 10
    yellow = 11

    @staticmethod
    def to_string(c: int) -> str:
        return [
            'blue',
            'brown',
            'darkgreen',
            'gray',
            'green',
            'lightblue',
            'lightgreen',
            'orange',
            'pink',
            'purple',
            'red',
            'yellow'
        ][c]
