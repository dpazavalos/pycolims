# Python Command Line Menu System (PyCoLiMS)
A command line menu, designed for user selection of provided data. Useful
 for user directing script mid run, specifying parameters from list, etc
 
User selects their entry using corresponding key as specified in parens
. Designed for easy number pad usage

If given a dictionary, pycolims will return key/s, allowing easy user input to call a dict value
	
### Installation

```
pip install pycolims
```

### Single Selection menu

```python
import pycolims
single = pycolims.Single()
selection =  single.run(['Zero', 'One', 'Two'])
#   (0) Zero 
#   (1) One 
#   (2) Two 
#   ( )  
#  (!!) Break
# 2
selection
# 'Two'
```

### Multi Selection Menu
```python
import pycolims
multi = pycolims.Multi()
selections = multi.run([x for x in range(5)])
#   (0)( ) 0 
#   (1)( ) 1 
#   (2)(*) 2 
#   (3)( ) 3 
#   (4)(*) 4 
#   ( )  
# (**) Select All (//) Clear All (><) Flip All (..) Return Selected (!!) Break
# ..
selections
# [[False, 0], [False, 1], [True, 2], [False, 3], [True, 4]]
for selected, entry in selections:
    if selected:
        print(entry)
# 2
# 4
```

When a multi pycolims is used, the menu returns the entire given array with each item converted to 
a tuple, with boolean inserted at [0] indicating selection status

```[[False, 0], [False, 1], [True, 2], [False, 3], [True, 4]]```
Pycolims will also recognize when given a format like above, and will
 display selected entries appropriately
 
#### Paging (More entries than can be shown on screen)

In the case of a large list passed, pycolims uses pointers to only display
 as many as can be seen. Use `+` and `-` to navigate

      (-) Prev Page
      (+) Next Page