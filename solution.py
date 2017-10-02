import collections  # imported to find duplcate values
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # The idea is to traverse through each Units , find Naked Twins then
    # remove those values from concerned elements of the same unit
    for unit in unitlist:
        digit = ''
        unit_pos = [box for box in unit if len(values[box]) == 2]  # get the location of elements with  2 digits
        unit_list = unit.copy()   # make a copy of complete unitlist we are working on.
        unit_values = []
        for p in unit_pos:
            unit_values.append(values[p])   # make a copy of complete values in unitlist
        z = dict(zip(unit_pos,unit_values)) # make a subset of dictionary for this particular unitset      
        
        value_occurrences = collections.Counter(z.values())
        filtered_dict = {key: value for key, value in z.items() if value_occurrences[value] == 2} # Duplicate numbers are found here

        for k in filtered_dict:  
            unit_list.remove(k)             # Removing Naked Twin's location from the unitlist
            digit = str(filtered_dict[k])   # Naked Twin values in string format
        for d in digit:             
            for u in unit_list:
                values[u] = values[u].replace(d,'')   # Hovering over the list to remove Naked Twins values
    return values
            

def cross(A, B):
    return [s+t for s in A for t in B]
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
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

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))
    #return search(grid)
    

if __name__ == '__main__':
    print('Sudoku no.1\n')
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid_values(diag_sudoku_grid))
    print('\nSudoku no.1 Solved \n')
    display(solve(diag_sudoku_grid))
    print('\nDesired result\n')
    solved_diag_sudoku = {'G7': '8', 'G6': '9', 'G5': '7', 'G4': '3', 'G3': '2', 'G2': '4', 'G1': '6', 'G9': '5',
                          'G8': '1', 'C9': '6', 'C8': '7', 'C3': '1', 'C2': '9', 'C1': '4', 'C7': '5', 'C6': '3',
                          'C5': '2', 'C4': '8', 'E5': '9', 'E4': '1', 'F1': '1', 'F2': '2', 'F3': '9', 'F4': '6',
                          'F5': '5', 'F6': '7', 'F7': '4', 'F8': '3', 'F9': '8', 'B4': '7', 'B5': '1', 'B6': '6',
                          'B7': '2', 'B1': '8', 'B2': '5', 'B3': '3', 'B8': '4', 'B9': '9', 'I9': '3', 'I8': '2',
                          'I1': '7', 'I3': '8', 'I2': '1', 'I5': '6', 'I4': '5', 'I7': '9', 'I6': '4', 'A1': '2',
                          'A3': '7', 'A2': '6', 'E9': '7', 'A4': '9', 'A7': '3', 'A6': '5', 'A9': '1', 'A8': '8',
                          'E7': '6', 'E6': '2', 'E1': '3', 'E3': '4', 'E2': '8', 'E8': '5', 'A5': '4', 'H8': '6',
                          'H9': '4', 'H2': '3', 'H3': '5', 'H1': '9', 'H6': '1', 'H7': '7', 'H4': '2', 'H5': '8',
                          'D8': '9', 'D9': '2', 'D6': '8', 'D7': '1', 'D4': '4', 'D5': '3', 'D2': '7', 'D3': '6',
                          'D1': '5'}
    display(solved_diag_sudoku)
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
