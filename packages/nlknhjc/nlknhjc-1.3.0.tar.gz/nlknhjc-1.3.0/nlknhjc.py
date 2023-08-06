"""the description"""


def nested_list(the_list, indent=False, level=0):
    """the description"""
    for item in the_list:
        if isinstance(item, list):
            nested_list(item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end="")
            print(item)
