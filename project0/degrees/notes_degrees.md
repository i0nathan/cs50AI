# CS50AI notes

## pset 1
[ Revised approach ]
Start with a frontier that contains the initial state
Repeat:
	If the frontier is empty, then there is no solution.
	Remove a node form the frontier
	If node contains goal state, return the solution
	Add the node to the explored set
	Expand node, add resulting nodes to the frontier if they aren't already in the frontier or the explored set

[ Cost function ]	
We need to iterate over the initial expanded node and calculate each of the possibilities costs
Update the lowest cost as a break point -> if find the solution or break point > lowest cost
Pass the updated frontier, selected node (from heuristic func), lowest cost, current cost, target, explored array

[ tried functions ]
This function returned too many and repeated nodes?
```python
def test(source, target, explored=[]):

    for x in neighbors_for_person(source):
        if target == x[1]:
            explored.append(x)
            return explored
        # Add to frontier
        elif x not in explored and x[1] != source:
            explored.append(x)

    for e in explored:
        return test(e[1], target, explored[1:])

    return None
```

- This function was tested with some effort of cost evaluation in shortest path function (below)
```python
def test2(source, target, explored=[]):

    for x in neighbors_for_person(source):
        if target == x[1]:
            explored.append(x)
            return explored
        # Add to frontier
        elif x not in explored and x[1] != source:
            explored.append(x)
            return test2(x[1], target, explored)

    return None
```
- from shortest path function
```python
    ############################################################################
    # Return trivial case
    if source == target: return explored

    # Look in all the neighbors
    for x in neighbors_for_person(source):
        if target == x[1]:
            explored.append(x)
            return explored
        # Add to frontier
        elif x not in explored and x[1] != source:
            explored.append(x)

    # Evaluate the cost of each neighbor to select shortest path
    for e in explored:
        lists.append(test2(e[1], target))

    shortest = float('inf')
    for i, l in enumerate(lists):
        if l == None: continue
        print(f"List {i} has {len(l)} elements")
        if len(l) < shortest:
            shortest = i

    print('\n' * 5)
    return lists[shortest]
```
	