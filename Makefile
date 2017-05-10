%.o: %.c
	gcc -Wall -o $@ $^

sphincs_distribution.pdf: authpath.py plot.py
	python3 -c "import plot; plot.plot_dist_sphincs()"

num_leaves.pdf: authpath.py plot.py
	python3 -c "import plot; plot.plot_num_leaves()"
