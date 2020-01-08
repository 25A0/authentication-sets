#include <stdlib.h>
#include <stdio.h>

/*
  This file contains a C implementation to generate the authentication
  set of a given set of leaf nodes, as well as some demo code to
  illustrate how it can be used.
 */

static int cmp(const void* a, const void* b)
{
  return *(unsigned long *)a - *(unsigned long *)b;
}

unsigned int ceil_log_2(unsigned int n)
{
  unsigned int r = 0;
  n = 2 * n - 1;
  for (; n; r++) {
    n >>= 1;
  }
  return r - 1;
}

unsigned int compute_worst_case_size(unsigned int height,
                                     unsigned int num_leaves)
{
  if(num_leaves == 0) return 0;

  // There are faster methods to compute the Hamming Weight and the logarithm
  // base 2 (https://graphics.stanford.edu/~seander/bithacks.html), but this
  // function has to be called only once per signature / verification, with
  // small*ish values for num_leaves, and is already in O(log_2(num_leaves)).

  // the lowest layer on which all leaves are children of different subtrees:
  // layer = h - ceil(log_2(num_leaves))
  //       = h + 1 - log_2(2 * num_leaves - 1)
  unsigned int layer = height -  ceil_log_2(num_leaves);

  unsigned int H; // Hamming-Weight of num_leaves - 1
  unsigned int x = num_leaves - 1;
  for (H=0; x; H++) {
    x &= x - 1;
  }

  return height + (num_leaves - 1) * layer - H;
}

/* Removes duplicates in sorted_leaves in-place and returns the number of
 * unique elements. As the name suggests, sorted_leaves should be sorted,
 * or at least have all duplicates in groups.
 */
unsigned int unique(unsigned int nleaves, unsigned long* sorted_leaves)
{
  if(nleaves > 1) {
    int i;
    unsigned int nunique = 1;
    unsigned long last = sorted_leaves[0];
    for(i = 1; i < nleaves; i++) {
      if(sorted_leaves[i] != last) {
        last = sorted_leaves[i];
        sorted_leaves[nunique++] = last;
      }
    }
    return nunique;
  } else {
    return nleaves;
  }
}

struct node {
  unsigned int level;
  unsigned long index;
};

/* Calculates the distance in layers between the leaf at index i1 and the
 * node that is the first common parent node of the leaves at index i1 and i2.
 */
unsigned int parent_distance(unsigned long i1, unsigned long i2)
{
  unsigned int d = 0;
  while(i1 != i2) {
    i1 >>= 1;
    i2 >>= 1;
    d++;
  }
  return d;
}

/* Calculates the authentication set for the given leaves.  auth_set should be
 * large enough to hold sufficient nodes for the worst-case scenario.
 */
unsigned int authentication_set(unsigned int nleaves, unsigned int height,
                                unsigned long* given_leaves,
                                struct node* auth_set)
{
  // Sort the given leaves in-place in ascending order
  qsort(given_leaves, nleaves, sizeof(unsigned long), cmp);
  // Remove duplicates
  unsigned int nunique = unique(nleaves, given_leaves);

  unsigned int nnodes = 0; // The number of nodes in the authentication set
  unsigned int stack[height]; // A stack that holds the layers on which no nodes
                              // need to be included.
  unsigned int* stackp = stack; // Pointer to the top of the stack

  int i;
  for(i = 0; i < nunique; i++) {
    unsigned long leaf = given_leaves[i];

    // distance to common parent of this leaf and the next leaf, if there is one
    unsigned int d = 0;
    if(i < nunique - 1) {
      d = parent_distance(leaf, given_leaves[i+1]);
    } else {
      d = height;
    }

    // Check for the first d-1 elements of the current leaf's authentication
    // path whether they're on the stack. If they are, pop them from the stack.
    // Otherwise add them to the authentication set.
    {
      int j;
      unsigned long index = leaf;
      for(j = 0; j < d - 1; j++) {
        // Check if the layer of this node is at the head of the stack
        if(stackp > stack && *(stackp-1) == j) {
          // pop that layer from the stack
          stackp--;
        } else {
          // add that node to the authentication set
          auth_set[nnodes].level = j;
          auth_set[nnodes].index = index ^ (unsigned long) 1; // flip the last bit
          nnodes++;
        }
        index >>= 1;
      }
    }

    // Calculate the layer of the node on this leaf's path that is the child of
    // the common parent, and push that layer to the stack
    *stackp = d - 1;
    stackp++;
  }
  return nnodes;
}

int main(int nargs, const char** args)
{
  unsigned int height = 16;
  unsigned int nleaves = 32;
  unsigned long given_leaves[nleaves];

  int i;

  // Populate the given leaves with the worst-case scenario
  unsigned int offset = 1 << (height - ceil_log_2(nleaves));
  for(i = 0; i < nleaves; i++) {
    given_leaves[i] = i * offset;
  }

  /*
  // Populate the given leaves with the best-case scenario
  for(i = 0; i < nleaves; i++) {
    given_leaves[i] = i;
  }
  */

  unsigned int worst_case_size = compute_worst_case_size(height, nleaves);

  struct node auth_set[worst_case_size];
  unsigned int nnodes = authentication_set(nleaves, height, given_leaves,
                                           auth_set);

  printf("auth set worst case size: %4d\n", worst_case_size);
  printf("sum of auth paths:        %4d\n", nleaves * height);
  printf("actual auth set size:     %4d\n", nnodes);
  printf("reduction by:              %6.2f%%\n", 100 * (1.0 - ((float) nnodes / (float) (nleaves * height))));
  // for(i = 0; i < nnodes; i++) {
  // printf("%d: level %d, index %ld\n", i, auth_set[i].level, auth_set[i].index);
  // }
  return 0;
}
