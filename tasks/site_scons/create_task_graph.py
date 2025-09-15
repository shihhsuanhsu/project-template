"""
Functions for creating a task graph using Graphviz.
"""


def create_task_graph(env):
    """
    Create a task graph using Graphviz.
    Assume working directory is the project tasks directory.
    """
    import os
    import re
    from SCons.Util import render_tree
    import graphviz

    # get the root node
    root_node = env.Dir(".")

    DEPS = {}
    """Store the children of each node"""

    def get_children(node):
        """
        Get the children of the node.
        """
        children = node.children()
        if children and node is not root_node:
            # stores the children of the node
            DEPS[str(node)] = set(map(str, children))
        return children

    # render the tree (stores the dependencies in `DEPS`)
    render_tree(root=root_node, child_func=get_children)

    # maintain only the task level dependencies
    task_deps = {}
    for node, children in DEPS.items():
        # ignore the task_graph node
        if node == ".":
            continue
        # get origin task name
        task_name = node.split("/")[0]
        if task_name not in task_deps:
            task_deps[task_name] = set()
        # get the children task names
        for child in children:
            child_task_name = child.split("/")[0]
            # don't add self dependency
            if child_task_name and child_task_name != task_name:
                # store the task level dependencies
                task_deps[task_name].add(child_task_name)

    # create the graph
    G = graphviz.Digraph(comment="Task Graph")
    G.graph_attr["rankdir"] = "LR"
    # draw the nodes
    for task in task_deps.keys():
        G.node(task)
    # draw the edges
    for task, deps in task_deps.items():
        # draw the edges
        for dep in deps:
            G.edge(dep, task)

    # store the graph
    G.render("task_graph/output/task_graph", format="png", cleanup=True)

    # attach the task graph to the SCons, so that it is cleaned with `scons -c`
    env.Clean(".", "task_graph/output/task_graph.png")
