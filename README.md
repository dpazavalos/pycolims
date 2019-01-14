# Python Command Line Menu Selector (PyCoLiMS)
A command line interface single stage menu system, designed to display a given list on screen and prompt the user to select from said list. Returns the selected item/s to the calling function in the same format as provided*

In the case of very large lists, PyCoLiMS breaks** the list down into terminal-sized chunks with a paging system, allowing lists larger than the screen to be processed without issue

Has single and multiple selection modes.

\* A note on Dictionaries: PyCoLiMS displays and returns only the keys of a dictionary. This allows easy user input to call a dict value

\*\* It's a series of pointers, not a bunch of new lists. PyCoLiMS tries to stay mem friendly!
	
### installation

    pip install pycolims

### Single Selection menu

    import pycolims
    menu_single = pycolims.SelectSingle()
    menu_single.run(array_in: Union[List[any], 
                                    Tuple[any], 
                                    Dict[any, any]], 
                    header: str="") -> Union[any, 
                                             List[any]]

Single selection menu returns the one item selected from array_in. This can be a single item or one nested list from array_in. 


### Multi Seletion Menu

    import pycolims
    menu_multi = pycolims.SelectMulti()
    menu_multi.run(array_in: Union[List[any], 
                                   List[List[bool, any]],
                                   Tuple[any], 
                                   Dict[any, any]], 
                    header: str="") -> List[List[bool, any]])

A note on SelectMulti: the multiple selection menu returns the entire array given to it with an embedded boolean prefixing each given item, indicating menu selection status. 

     print([val for [val, boolean] in menu_multi.run(arr) if boolean])

Also of note, SelectMulti is able to parse a given list in the same format, allowing a menu to start with values already indicated

    prev_settings = [[True, val_one], 
                     [False, val_two]]


### Final notes

This project is still quite young; notable ToDos include wider type acceptance and confirmed stress testing.

This project was inspired by old school "Green Screen" programs used on retail thin clinents. These lightweight programs always facinated me, and I loved navigating to deep submenus with a series of quick keystrokes.

PyCoLiMS is still quite young; all feedback is appreciated. 