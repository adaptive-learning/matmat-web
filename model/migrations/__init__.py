def get_children(skill):
    # using DFS to avoid infinite loops in case child is also a parent
    fringe = [skill]
    children = set([skill])

    while fringe:
        node = fringe.pop(0)
        for ch in node.children.all():
            if ch not in children:
                fringe.append(ch)
                children.add(ch)

    return list(children)
