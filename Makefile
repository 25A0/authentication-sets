%.o: %.c
	gcc -Wall -o $@ $^

figures/sphincs_distribution.pdf: authpath.py plot.py
	python3 -c "import plot; plot.plot_dist_sphincs()"

figures/num_leaves.pdf: authpath.py plot.py
	python3 -c "import plot; plot.plot_num_leaves()"
