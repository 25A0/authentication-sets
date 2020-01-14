# Authentication sets

Code and statistics related to authentication sets can be found here.

 - [authset.py](./authset.py) contains a Python implementation of
   authentication sets, as well as code to run tests to compare authentication
   sets to the original optimization used in SPHINCS.
   Run `python3 authset.py` to run tests on the performance of authentication sets.
 - [authset.c](./authset.c) contains a C implementation of authentication sets,
   and some demo code to illustrate how to use it.
 - [plot.py](./plot.py) contains code to produce the plots in this README
 - [measure.py](./measure.py) contains code to export test data as a csv

This work is part of my master's thesis, which is yet to be published.
More information related to authentication sets will be available in there.

## What are authentication sets?

Authentication sets compress the
authentication paths of multiple leaf nodes in a binary
hash tree.

Alice has a [binary hash tree](https://en.wikipedia.org/wiki/Merkle_tree) of
height h. Bob only knows the root of the tree. Now, Alice wants to prove to Bob
that a specific leaf node, n, is part of the tree. To do this, she can reveal
the
[authentication path](https://en.wikipedia.org/wiki/Merkle_signature_scheme#/media/File:MerkleTree2.1.svg)
of the leaf node to Bob. The authentication path of a leaf node n is the
smallest set of nodes that, together with n, can be used to restore the root
node of the tree.

To authenticate more than one leaf node, Alice can simply send Bob the
authentication paths of all those leaf nodes. However, as soon as more than one
leaf node needs to be authenticated, there will always be some redundancy
between the authentication paths: Different paths may contain the same node,
making it redundant, or the information in one path may allow the computation
of a node required in another path. Authentication sets are a way to utilise
this redundancy.

Authentication sets are never bigger, and usually smaller than the combined
size of the authentication paths. The following graph shows how their size
compares to the combined size of the authentication paths, in a tree of
height 16. For example, if 16 leaf nodes are given, authentication sets are on
average 30% smaller than the sum of the authentication paths.

![A graph that compares the size of the authentication path to the size of the sum of the authentication sets, for varous numbers of given leaf nodes. The graph shows that authentication sets become increasingly small compared to the sum of authentication sets, the more leaf nodes are given.](num_leaves.png)

In the best case scenario, authentication sets can be drastically smaller than
the sum of the authentication paths. For example, in a binary tree of height
16, with 32 revealed leaf nodes, authentication sets can be as small as 11
nodes, while the separate authentication paths have a combined size of 16 * 32
= 512 nodes. In reality, however, the size of authentication sets is usually
closer to the worst-case size. The following graph shows how the size of
authentication sets are distributed for 32 given leaf nodes in a tree of height
16:

![A histogram that shows the distribution of authentication set sizes for various samples of 32 given leaf nodes in a tree of height 16. The histogram shows that the average sample size lies between 320 and 330 nodes, and that barely any samples have a size smaller than 300 nodes.](sphincs_distribution.png)

Nonetheless, here the worst-case size of the authentication set, 352 nodes, is
still significantly smaller than the combined size of the separate
authentication paths (512 nodes), and still smaller than the optimization used
in SPHINCS, which uses 384 nodes.
