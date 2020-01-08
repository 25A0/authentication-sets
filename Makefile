%.o: %.c
	gcc -Wall -o $@ $^

sphincs_distribution.png: authpath.py plot.py
	python3 -c "import plot; plot.plot_dist_sphincs('$@')"

num_leaves.png: authpath.py plot.py
	python3 -c "import plot; plot.plot_num_leaves('$@')"

size_distribution.csv: authpath.py measure.py
	python3 -c "import measure; measure.measure_dist_sphincs('$@')"

num_leaves.csv: authpath.py measure.py
	python3 -c "import measure; measure.measure_num_leaves('$@')"
