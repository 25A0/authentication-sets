#include <stdlib.h>
#include <stdio.h>

static int cmp(const void* a, const void* b)
{
  return *(unsigned long *)a - *(unsigned long *)b;
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

/* Calculates the authentication set for the given leaves.  auth_set should be
 * large enough to hold height * nleaves nodes (TODO: adjust this to the #
 * nodes in the worst case scenario)
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
  struct node stack[height]; // A stack that holds nodes that do not need to be
                             // included in the authentication set
  struct node* stackp = stack; // Pointer to the top of the stack

  // For all but the last leaf:
  int i;
  for(i = 0; i < nunique - 1; i++) {
    unsigned long leaf = given_leaves[i];

    // distance to common parent of this leaf and the next leaf
    unsigned int d = 0;
    {
      unsigned long current = leaf;
      unsigned long next = given_leaves[i+1];
      while(current != next) {
        current >>= 1;
        next >>= 1;
        d++;
      }
    }

    // Add the first d-1 elements of the current leaf's authentication path to
    // the authentication set
    {
      int j;
      unsigned long index = leaf;
      for(j = 0; j < d - 1; j++) {
        auth_set[nnodes].level = j;
        auth_set[nnodes].index = index ^ (unsigned long) 1; // flip the last bit
        nnodes++;
        index >>= 1;
      }
    }

    // Calculate the node on this leaf's path that is the child of the common
    // parent, and push that to the stack
    stackp->level = d - 1;
    stackp->index = leaf >> (d - 1);
    stackp++;
  }

  // Finally, for the last leaf: Add each node of the authentication path of
  // this leaf to the authentication set, unless it's on the stack.
  int stack_count = stackp - stack;
  stackp--; // Point to last pushed element
  int j;
  unsigned long index = given_leaves[nunique - 1];
  for(j = 0; j < height; j++) {
    index ^= (unsigned long) 1;
    if(stack_count > 0 && stackp->level == j && stackp->index == index) {
      // Pop that element from the stack
      stackp--;
    } else {
      // Add that element to the authentication set
      auth_set[nnodes].level = j;
      auth_set[nnodes].index = index;
      nnodes++;
    }
    index >>= 1;
  }

  return nnodes;
}

int main(int nargs, const char** args)
{
  unsigned long given_leaves[] = {1, 4, 7};
  unsigned int nleaves = 3;
  unsigned int height = 3;
  struct node auth_set[height * nleaves];
  unsigned int nnodes = authentication_set(nleaves, height, given_leaves,
                                           auth_set);
  int i;
  printf("# nodes: %d\n", nnodes);
  for(i = 0; i < nnodes; i++) {
    printf("%d: level %d, index %ld\n", i, auth_set[i].level, auth_set[i].index);
  }
  return 0;
}
