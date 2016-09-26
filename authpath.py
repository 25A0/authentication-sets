from random import randint

def authpath(index, height):
    # Current layer
    layer = 0
    authpath = []
    while layer < height:
        if index % 2 == 0:
            authpath.append((layer, index + 1))
        else:
            authpath.append((layer, index - 1))
        layer += 1
        index >>= 1

    return authpath

def path(index, height):
    # Current layer
    layer = 0
    path = []
    while layer < height:
        path.append((layer, index))
        layer += 1
        index >>= 1

    return path

def pick_leaves(numleaves, height):
    leaves = []
    for i in range(0, numleaves):
        leaves.append(randint(0, 2**height))
    return leaves

def sample(numleaves, height):
    leaves = pick_leaves(numleaves, height)
    accum_path = []
    accum_auth = []
    for leaf in leaves:
        accum_path += path(leaf, height)
        accum_auth += authpath(leaf, height)

    combined_path = set(accum_auth) - set(accum_path)

    # print("Given leaves: " + str(leaves))
    # print("Combined auth path:\n")
    # for node in combined_path: print(str(node) + " ")
    # print("Length of separate paths: {}".format(numleaves * height))
    # print("Length of combined path: {}".format(len(combined_path)))
    return len(combined_path)

def test():
    tests = 2**16
    numleaves = 32
    height = 16
    results = [sample(numleaves, height) for test in range(0, tests)]
    print("# leaves: {}".format(numleaves))
    print("height: {}".format(height))
    print("# samples: {}".format(tests))
    print("Length of separate paths: {}".format(numleaves * height))
    print("Combined paths:")
    print("Min: {}".format(min(results)))
    print("Max: {}".format(max(results)))
    print("Avg: {}".format(sum(results) / len(results)))

if __name__ == '__main__':
    numleaves = 32;
    height = 16;
    #sample(numleaves, height)
    test()
