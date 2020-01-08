%.o: %.c
	gcc -Wall -o $@ $^

figures/sphincs_distribution.pdf: authpath.py plot.py
	python3 -c "import plot; plot.plot_dist_sphincs('$@')"

figures/num_leaves.pdf: authpath.py plot.py
	python3 -c "import plot; plot.plot_num_leaves('$@')"

size_distribution.csv: authpath.py measure.py
	python3 -c "import measure; measure.measure_dist_sphincs('size_distribution.csv')"

num_leaves.csv: authpath.py measure.py
	python3 -c "import measure; measure.measure_num_leaves('num_leaves.csv')"
