
from utils import *
import itertools


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
##unitlist = unitlist


##The diagonals should be 
## 1) [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
## 2) [['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
## 3) if diagonal is chosen it should be part of unit list since it will be considered a peer

## create the first diagonal
diagonal_units_1 = [[rows[i]+cols[i] for i in range(len(rows))]]
## Reverse the column index
cols_reverse = cols[::-1]
## create the second diagonal
diagonal_units_2 = [[rows[i]+cols_reverse[i] for i in range(len(rows))]]

is_diagonal = False 
#if diagonal is true, add the diagonals to unitlist to be considered as peers
if (is_diagonal == True):
    unitlist = row_units + column_units + square_units + diagonal_units_1 + diagonal_units_2
else:
    ##If the variable is false, diagonals are not part of being peers
    unitlist = row_units + column_units + square_units


units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    # Find all instances of naked twins in every square unit
    ## the first 9 unit_square are rows
    ## the second 9 unit_square are columns
    ## the third 9 unit_square are units
    ## the last 2 unit_square are diagonals        
    for unit_square in unitlist:
        box_values = [(values[box], box) for box in unit_square if len(values[box]) == 2]
        if(box_values):
            ##Get all the possible combinations
            combination_pairs = list(itertools.combinations(box_values, 2))
            for pair in combination_pairs:
                box_value1 = pair[0][0]
                box_index1 = pair[0][1]                
                box_value2 = pair[1][0];
                box_index2 = pair[1][1]                
                ## if in the same unit there exists
                ## then replace it
                if(box_value1 == box_value2):
                    for u in unit_square:
                        if(u != box_index1 and u != box_index2):
                            n, t = box_value1[0], box_value1[1]
                            assign_value(values, u, values[u].replace(n, ''))
                            assign_value(values, u, values[u].replace(t, ''))                        
    return values     
    
    ##raise NotImplementedError


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    # code help from : udacity    
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
#         for peer in peers[box]:
        for peer in peers[box]:
#             if(not len(values[peer]) == 1):
            values[peer] = values[peer].replace(digit,'')
    return values    
    ##raise NotImplementedError


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    # code help from : udacity
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values    
    
    ##raise NotImplementedError


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    # code help from : udacity    
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        values = naked_twins(values)
        
        #values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    
    ##raise NotImplementedError


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    # code help from : udacity    
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt    
    ##raise NotImplementedError
def assign_value(values, box, value):
    """
    Params: 
    values = All square units of the entire sudoku
    box: Index of the square box example: A1, A2, G3...
    value: 
    """
    values[box] = value
    return values

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    
#     diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
#     diag_sudoku_grid = '.......41......89...7....3........8.....47..2.......6.7.2........1.....4..6.9.3..'
#     diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
#     diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#     diag_sudoku_grid = '9682.7.31.........7..39....3....2.17.........18.9....6....31..5.........41.7.5368'
    diag_sudoku_grid = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
        
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
