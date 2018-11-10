import shutil


# # # Menu Testing
# # # Given a list of options, cultivate a multipage system with prev/next/back options
# (8) Prev Page
# (9) Next Page
# (0) Go Back


def holder():
    # def play_again(self, prompt=''):
    prompt = ''
    while prompt not in '0 1'.split():
        prompt = input("\n(0) Quit \n(1) Run again \n> ")
    repeating = prompt is '1'
    print(repeating)


def split_list(target, tar_max):
    out = []
    for i in range(0, len(target), tar_max):
        out.append(target[i:i + tar_max])
    return out


def displayer(inlist, navopts):
    to_display = []
    valid_selections = []
    valid_navopts = []

    # gen list of valid options
    for x in inlist:
        to_display.append(x)
        valid_selections.append(str(x))

    # visual indication of selections end and nav begin
    to_display.append([' ', '----------'])

    # add nav options
    for opt in navopts:
        to_display.append(opt)
        if opt[0] is not " ":
            valid_navopts.append(opt[0])

    # stdout
    for each in to_display:
        print(f'({each[0]})'.rjust(4), each[1])

    prompt = ''
    while prompt not in valid_selections or prompt.lower not in valid_navopts:
        prompt = input()
        return prompt


def navigator(menu_list):

    # Index all of the single menu's values
    ndx = 0
    for x in menu_list:
        menu_list[ndx] = [ndx, x]
        ndx += 1

    # Determine chunk size to split menu list into, based off terminal size
    # if list is shorter than columns avail, simply use list
    height = shutil.get_terminal_size()[1]
    # height = max(shutil.get_terminal_size()[1], len(menu_list))
    valids_for_menu = split_list(menu_list, height - 6)  # Subtact 6 to allow space for nav options, input line, etc

    # Determine first and last indexes of inlist
    first_page_ndx = valids_for_menu[0]
    last_page_ndx = len(valids_for_menu) - 1

    # Bottom of page navigator options
    # [7, "Prev Page"]
    # [8, "Next Page"]
    # [9, "Go Back"]

    # Used to determine which chunk of menu_list to unpack
    goto_ndx = 0
    goto_figure = 0  # val returned by sort_for_mprint

    while goto_figure != ".":

        print("\n" * height)

        # (ToDo: When integrating into classes, store nav options as self.vars)
        if len(valids_for_menu) <= 1:
            goto_figure = displayer(valids_for_menu[goto_ndx], [[" ", ""],
                                                                [" ", ""],
                                                                [".", "Go Back"]])

        elif goto_ndx != 0 and goto_ndx != last_page_ndx:
            goto_figure = displayer(valids_for_menu[goto_ndx], [["-", "Prev Page"],
                                                                ["+", "Next Page"],
                                                                [".", "Go Back"]])
        elif goto_ndx == 0:
            goto_figure = displayer(valids_for_menu[goto_ndx], [[" ", ""],
                                                                ["+", "Next Page"],
                                                                [".", "Go Back"]])
        elif goto_ndx == last_page_ndx:
            goto_figure = displayer(valids_for_menu[goto_ndx], [["-", "Prev Page"],
                                                                [" ", ""],
                                                                [".", "Go Back"]])

        if goto_figure is "-":
            goto_ndx -= 1
            if goto_ndx < 0:
                goto_ndx = 0

        elif goto_figure == "+":
            goto_ndx += 1
            if goto_ndx > last_page_ndx:
                goto_ndx -= 1

    # print menu
    # for x in setlist:
    #     mprint(x[0], x[1])


test = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
navigator(test)
