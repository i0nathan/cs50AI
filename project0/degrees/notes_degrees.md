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

- Recursive function seems to work but in the large dataset exceeds the allowed recursion limit
```python
def recursive_search(source, target, frontier, explored):
    # We can ignore the frontier and nodes utils and use simple arrays
    # Return the explored array when found
    if frontier.empty(): return None

    node = frontier.remove()
    if node.action != None: explored.append((node.action, node.state))
    if node.state == target: return []

    shortest_path = None
    # finder = None
    # path = []

    for a in neighbors_for_person(node.state):
        if a not in frontier.frontier and a not in explored:  # can find (movie, star) in frontier.frontier?
            frontier.add(Node(a[1], node.state, a[0]))
        # try:
        #     finder = recursive_search(target, frontier, explored)
        # except TypeError:
        #     pass

        # TODO: get rid of any unnecesary items
        finder = recursive_search(source, target, frontier, explored)
        if finder != None:
            if len(finder) > 0:
                if any(x[1] == source for x in neighbors_for_person(finder[0][1])):  # If source is in common
                        return finder
            if len(finder) > 1:
                # check if current node can replace a finder node
                for i in range(len(finder) - 1):
                    if finder[i+1] in neighbors_for_person(a[1]):
                        finder.pop(0)
            return [a] + finder
            # path = finder + [a]
            # print(path)
            # if shortest_path == None or len(path) < len(shortest_path):
            #     shortest_path = path

        # Reverse connect to source: if source in neighbors of finder i
        # if finder != None:  # Target item
        #     path = finder + [a]



    return shortest_path
```
	
neighbor of source: neighbors_for_person('102'): {('104257', '193'), ('112384', '158'), ('104257', '129'), ('104257', '102'), ('112384', '102'), ('104257', '197'), ('112384', '200'), ('112384', '641')}	
explored = [('104257', '193'), ('104257', '197'), ('104257', '129'), ('95953', '163'), ('95953', '420'), ('95953', '596520'), ('95953', '129'), ('104257', '102'), ('112384', '158'), ('109830', '705')]
shortest_path = [('109830', '705')]