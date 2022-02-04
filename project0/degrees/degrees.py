import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


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


def expand(frontier):
    if frontier.empty(): return None
    if frontier.contains_state(target): return explored
    explored.append(frontier.remove())

    frontier.add(Node(state=n[1], parent=source, action=neighbors_for_person(n[1])))


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO
    # source: Kevin Bacon > target: Robin Wright
    # For movie in people['movies'] if source in movies[m]['stars'] return steps, else steps++
    # Apolo 13 (Kevin Bacon [102], Tom Hnaks [158]) > Forest Gump (Tom Hanks [158], Robin Wright [705])
    # [(112384, 158), (109830, 705)]

    # Node:
    #     state = movie, id
    #     parent = node that generated this node
    #     action = action applied to parent node to get to this state

    # TODO: Last node is not needed, returning too many nodes

    # Initialize explored list
    explored = []

    # Identify movies of target
    target_movies = people[target]["movies"]

    frontier = StackFrontier()

    # Add initial node
    frontier.add(Node(source, None, None))

    while not frontier.empty():
        # if frontier.contains_state(target): return explored

        # Allow to look for specific params in frontier
        heu = len(frontier.frontier) - 1

        # Remove node that has movie same as target movies
        for i, n in enumerate(frontier.frontier):
            if n.state == target:
                explored.append((n.action, n.state))
                return explored
            # if node neighbor has a movie from those in target, search that first
            # if n.action in target_movies and not any(x[1] == n.state for x in explored):
            if n.action in target_movies:
                heu = i
                # node = frontier.frontier.pop(i)
                # break
        node = frontier.frontier.pop(heu)
        # node = frontier.remove()

        # Add explored nodes except first node
        if node.action != None:
            explored.append((node.action, node.state))

        for a in neighbors_for_person(node.state):
            if (a not in explored) and ((a[0], a[1]) not in frontier.frontier) and (a[1] != node.state):
                frontier.add(Node(a[1], node.state, a[0]))

    return None

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


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
