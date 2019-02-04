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

