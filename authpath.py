from random import randint

def auth_path(index, height):
    """Return the authentication path for a leaf at the given index.

    Keyword arguments:
    index  -- the leaf's index, in range [0, 2^height - 1]
    height -- the height of the binary hash tree

    Returns:
    The authentication path of the leaf at the given index as a list of nodes.
    Each node is represented as a tuple consisting of the node's layer, and the
    node's index within this layer.
    """
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
    """Return the path from a leaf to the root of a binary hash tree.

    Keyword arguments:
    index  -- the leaf's index, in range [0, 2^height - 1]
    height -- the height of the binary hash tree

    Returns:
    The path from the leaf at the given index to the root of the binary tree as
    a list of nodes. Each node is represented as a tuple consisting of the
    node's layer, and the node's index within this layer.
    """
    # Current layer
    layer = 0
    path = []
    while layer < height:
        path.append((layer, index))
        layer += 1
        index >>= 1

    return path

def pick_leaves(numleaves, height):
    """Randomly select a number of leaves of a binary hash tree.

    Keyword arguments:
    numleaves -- the number of leaves that will be selected
    height    -- the height of the binary hash tree

    Returns:
    A list of numleaves indices in range [0, 2^height - 1]
    """
    # Best case scenario:
    # leaves = range(0, numleaves)

    # Worst case scenario:
    # spacing = 2**height / numleaves
    # leaves = [i * spacing for i in range(0, numleaves)]

    # Random leaves:
    leaves = []
    for i in range(0, numleaves):
        leaves.append(randint(0, 2**height))
    return leaves

# Calculates and returns the authentication set of the given leaves
# in a binary tree of the given height.
# _cut_
def auth_set(leaves, height, cut=0):
    """Return the authentication set of the given leaves.

    Keyword arguments:
    leaves -- the set of given leaves as a list of indices in
              range [0, 2^height-1]
    height -- the height of the binary hash tree
    cut    -- (optional) If cut is specified, cuts off the given number
              of levels from the top of the tree. This removes all nodes
              above the cut off leve, and all nodes on the cut off level.
              This mimics the optimisation that is applied in SPHINCS at
              level 10.

    Returns:
    The minimal list of nodes that is needed to restore the root of the binary
    hash tree from the given leaves. Each node is represented as a tuple
    consisting of the node's layer, and the node's index within this layer.
    """
    accum_path = []
    accum_auth = []
    for leaf in leaves:
        accum_path += path(leaf, height)
        accum_auth += auth_path(leaf, height)

    # Remove duplicates and remove all nodes that are
    # present on the path to any given leaf
    combined_path = set(accum_auth) - set(accum_path)

    if cut > 0:
        # Remove all elements that are higher than layer height - cut
        reduced_path = [(i, j) for (i, j) in combined_path if i < height - cut]
        # Add all elements on layer height - cut
        reduced_path += [(height - cut, i) for i in range(0, 2**cut)]
    else:
        reduced_path = combined_path

    # print("Given leaves: " + str(leaves))
    # print("Combined auth path:\n")
    # for node in combined_path: print(str(node) + " ")
    # print("Length of separate paths: {}".format(numleaves * height))
    # print("Length of combined path: {}".format(len(combined_path)))
    return reduced_path

def measure(tests, numleaves, height, cut):
    """Measure the size of the authentication set.

    Keyword arguments:
    tests     -- the number of tests
    numleaves -- the number of given leaves
    height    -- the height of the binary hash tree
    cut       -- the number of levels that are cut off the top of the tree

    Prints various statistics summarising the measurement.
    """
    # Accumulate the test results
    results = [len(auth_set(pick_leaves(numleaves, height), height, cut))
               for test in range(0, tests)]
    print("# leaves: {}".format(numleaves))
    print("height: {}".format(height))
    print("cut: {}".format(cut))
    print("# samples: {}".format(tests))
    print("Length of separate paths: {}".format(numleaves * height))
    print("Combined paths:")
    print("Min: {}".format(min(results)))
    print("Max: {}".format(max(results)))
    print("Avg: {}".format(sum(results) / len(results)))

if __name__ == '__main__':
    tests = 2**14
    numleaves = 32
    height = 16
    cut = 0
    #sample(numleaves, height, cut)
    measure(tests, numleaves, height, cut)
