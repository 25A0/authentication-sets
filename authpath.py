#!/usr/bin/env python3
from random import randrange

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
        authpath.append((layer, index ^ 1))
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
        leaves.append(randrange(0, 2**height))
    return leaves

# Naive implementation. See authpath.c for fast implementation
def naive_auth_set_indices(leaves, height):
    """Return the authentication set of the given leaves.

    The authentication set is the minimal set of nodes necessary to restore the
    root of the binary hash tree from the given leaves.

    Keyword arguments:
    leaves -- the set of given leaves as a list of indices in
              range [0, 2^height-1]
    height -- the height of the binary hash tree

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

    return combined_path

def half_dist(l1, l2):
    """Return half of the geodesic distance between the two leaves l1 and l2.

    This is at the same time the distance from either leaf to their first
    common parent.

    Keyword arguments:
    l1, l2 -- the indices of the two leaves

    Returns:
    The geodesic distance (i.e. the number of edges on the shortes path)
    from either leaf to the closest common parent node of both leaves.
    In particular, returns 0 if l1 == l2.
    """
    d = 0
    while l1 != l2:
        l1 >>= 1
        l2 >>= 1
        d += 1
    return d

def unique(sorted_list):
    """Return a new list containing all unique elements in their original order

    Keyword arguments:
    sorted_list -- a list of comparable elements in which all duplicates are
                   next to one another
    """
    res = []
    last = None
    for element in sorted_list:
        if last != element:
            # Add it to the result list
            res.append(element)
            # Skip all following instances of this element
            last = element

    return res

# Efficient implementation
def efficient_auth_set_indices(leaves, height):
    """Return the authentication set of the given leaves.

    The authentication set is the minimal set of nodes necessary to restore the
    root of the binary hash tree from the given leaves.

    Keyword arguments:
    leaves -- the set of given leaves as a list of indices in
              range [0, 2^height-1]
    height -- the height of the binary hash tree

    Returns:
    The minimal list of nodes that is needed to restore the root of the binary
    hash tree from the given leaves. Each node is represented as a tuple
    consisting of the node's layer, and the node's index within this layer.
    """
    sorted_unique_leaves = unique(sorted(leaves))
    stack = []
    auth_set = []

    for i in range(0, len(sorted_unique_leaves)):
        if i < len(sorted_unique_leaves) - 1:
            d = half_dist(sorted_unique_leaves[i],
                          sorted_unique_leaves[i+1])
        else:
            d = height + 1

        leaf_index = sorted_unique_leaves[i]
        for h in range(0, d - 1):
            if len(stack) > 0 and stack[-1] == h:
                stack.pop()
            else:
                # Add that element to the authentication set
                auth_set.append((h,leaf_index ^ 1))
            leaf_index >>= 1
        # Add that height to the stack
        stack.append(d-1)
    return auth_set

def trim(set, height, level):
    """Trim the given set to the given level and add all nodes of that level.

    Removes all nodes in the given set that are above the given level, and add
    all nodes of the given level. In cases where the set contains a lot of
    duplicate nodes in upper levels, this can reduce the overall size of the
    set.

    This optimiszation is applied in SPHINCS at level 10 in a binary tree of
    height 16.

    Keyword arguments:
    set -- the set of nodes, where each node is represented as a tuple
           consisting of the node's layer and the node's index within this layer
    height -- the height of the binary hash tree
    level -- the level at which to trim the set

    """
    cut = height - level
    if cut > 0:
        # Remove all elements that are at or higher than the given level
        reduced_set = [(i, j) for (i, j) in set if i < level]
        # Add all elements on that level
        reduced_set += [(level, i) for i in range(0, 2**cut)]
        return reduced_set
    else:
        return set

def sample_authset(numleaves, height, function):
    """Sample the size of an authentication set.

    Keyword arguments:
    numleaves -- the number of given leaves which will be picked randomly
    height    -- the height of the binary hash tree
    function  -- the function that is used to sample the result. Should be
                 naive_auth_set or efficient_auth_set, or another function
                 with the same signature

    Returns:
    The length of the generated authentication set.
    """
    leaves = pick_leaves(numleaves, height)
    authset = function(leaves, height)

    return len(authset)

def sample_sphincs(numleaves, height):
    """Sample the size of the authentication paths as produced by SPHINCS.

    Keyword arguments:
    numleaves -- the number of given leaves which will be picked randomly
    height    -- the height of the binary hash tree

    Returns:
    The overall number of nodes stored by SPHINCS to authenticate the given
    number of leaves
    """
    leaves = pick_leaves(numleaves, height)
    accum_auth = []
    for leaf in leaves:
        accum_auth += auth_path(leaf, height)
    trimmed_set = trim(accum_auth, height, 10)

    return len(trimmed_set)

def measure(tests, numleaves, height):
    """Measure the size of the authentication set.

    Keyword arguments:
    tests     -- the number of tests
    numleaves -- the number of given leaves
    height    -- the height of the binary hash tree

    Prints various statistics summarising the measurement.
    """
    # Accumulate the test results
    results_naive_authsets = [sample_authset(numleaves, height, naive_auth_set_indices)
                              for test in range(0, tests)]
    results_efficient_authsets = [sample_authset(numleaves, height, efficient_auth_set_indices)
                                  for test in range(0, tests)]
    results_sphincs  = [sample_sphincs(numleaves, height)
                        for test in range(0, tests)]
    print("# leaves: {}".format(numleaves))
    print("height: {}".format(height))
    print("# samples: {}".format(tests))
    print("Length of separate paths: {}".format(numleaves * height))
    print("Authentication sets: (naive)")
    print("Min: {}".format(min(results_naive_authsets)))
    print("Max: {}".format(max(results_naive_authsets)))
    print("Avg: {}".format(sum(results_naive_authsets) / len(results_naive_authsets)))
    print("Authentication sets: (efficient)")
    print("Min: {}".format(min(results_efficient_authsets)))
    print("Max: {}".format(max(results_efficient_authsets)))
    print("Avg: {}".format(sum(results_efficient_authsets) / len(results_efficient_authsets)))
    print("SPHINCS:")
    print("Min: {}".format(min(results_sphincs)))
    print("Max: {}".format(max(results_sphincs)))
    print("Avg: {}".format(sum(results_sphincs) / len(results_sphincs)))

if __name__ == '__main__':
    tests = 2**14
    numleaves = 32
    height = 16
    measure(tests, numleaves, height)
