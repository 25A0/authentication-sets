%.o: %.c
	gcc -Wall -o $@ $^

sphincs_distribution.png: authset.py plot.py
	python3 -c "import plot; plot.plot_dist_sphincs('$@')"

num_leaves.png: authset.py plot.py
	python3 -c "import plot; plot.plot_num_leaves('$@')"

size_distribution.csv: authset.py measure.py
	python3 -c "import measure; measure.measure_dist_sphincs('$@')"

num_leaves.csv: authset.py measure.py
	python3 -c "import measure; measure.measure_num_leaves('$@')"
