"""the description"""


def nested_list(the_list, level):
    """the description"""
    for item in the_list:
        if isinstance(item, list):
            nested_list(item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end="")
            print(item)
