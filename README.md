# Python Command Line Menu Selector (PyCoLiMS)
A command line menu, designed for single stage selection.
Displays a given list on screen for user to select, either in single or multi mode.
Returns selected item/s to the calling function in the same format as provided.

If given a dictionary, pycolims will return key/s, allowing easy user input to call a dict value

In the case of lists too large to display at once, pycolims breaks the list down into terminal-sized
 chunks, with a paging system to cycle between the chunks 

\* It's a series of pointers, not a bunch of new lists. Pycolims tries to stay memory friendly!
	
### Installation

```
pip install pycolims
```

### Single Selection menu

```python
import pycolims
menu_single = pycolims.Single()
menu_single.run(array_in, header: str="")
```

A single selection menu will display items on screen and return a single user selected value
This can be a single item or one nested list from a given matrix 

### Multi Selection Menu
```python
import pycolims
menu_multi = pycolims.Multi()
menu_multi.run(array_in, header: str="")
```

When a multi pycolims is used, the menu returns the entire given array with each item converted to 
a list, where [0] is a boolean indicating selection
 
```python
 >>> list_with_booleans = menu_multi.run([0, 1, '2'])
 # User selects first and last options...
 >>> print(list_with_booleans)
 [[True, 0], [False, 1], [True, '2']]
```

Multi pycolims can also parse a given list in similar format to display items 'already selected'
 
```python
prev_settings = [[True, 'val_one'], 
                 [False, 'val_two']]
```

#### Pycolims menu options

Each pycolims menu has a series of commands at the bottom

    Single menu options
      (-) Prev Page
      (+) Next Page
      (!!) Break

    Multi Menu Options
      (-) Prev Page
      (+) Next Page
      (**) Select All (//) Clear All (><) Flip All (..) Return Selected (!!) Break

(-) Prev Page
(+) Next Page

Cycles through available pages

(!!) Break

Easy back out for end user use; throws a Keyboard interrupt error to interrupt code

(**) Select All (//) Clear All

Selects/Clears ALL available items

(><) Flip All

Inverts all item selections

(..) Return Selected

Finishes a multi selection menu and returns items
