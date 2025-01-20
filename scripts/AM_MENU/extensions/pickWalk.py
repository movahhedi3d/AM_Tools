import maya.cmds as mc



def get_all_tag_children(node):
    """Gets all child tag controls from the given tag node

    Args:
        node (str): Name of controller object with tag

    Returns:
        list: List of child controls (Maya transform nodes)
    """

    # store child nodes
    children = []

    # gets first child control
    child = mc.controller(node, query=True, children=True)

    # loop on child controller nodes to get all children
    while child is not None:
        children.extend(child)
        tags = []
        for c in child:
            tag = mc.ls(mc.listConnections(c, type="controller"))
            tags.extend(tag)
            if mc.listConnections("{}.parent".format(tag[0])) == node:
                return children
        child = mc.controller(tags, query=True, children=True)

    return children
