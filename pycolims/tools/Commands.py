"""Storage for display commands. Used by displayer"""


class DisplayCmd:

    turners = {
        ' ': " ",
        '-': "Prev Page",
        '+': "Next Page",
    }
    """Possible menu choices to change pages"""

    options = {
        '**': "Select All",
        '!!': "Clear All",
        '..': "Return Selected",
        '<>': "Break",
    }
    """Possible menu choices to change pages"""

    turners_inv = {val: key for key, val in turners.items()}
    """Dict enforcement of page turner; call by Values"""

    options_inv = {val: key for key, val in options.items()}
    """Dict enforcement of page turner; call by Values"""
