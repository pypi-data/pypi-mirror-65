def echo_indented_list(item, level=0):
    for x in item:
        if isinstance(x, list):
            echo_indented_list(x, level + 1)
        else:
            print("\t"*level + str(level) + ": -> ", end="")
            print(x)
