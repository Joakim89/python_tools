from helpers import *
from progress import ProgressBar

# read a pghw export file
headers, columns = read_PGHW_export("T7202006180003.tsd.gpsimp.txt")

# do a moving average on all the data with length 3000 (and use progressbar)
pb = ProgressBar(len(columns))
columns_ma = []
for i in range(0, len(columns)):
    columns_ma.append(moving_avg_fast(columns[i], 3000))
    pb += 1

# phase shift height 5 seconds
x_phase_height, y_phase_height = phase_shift(columns[0], columns[4], 5000)

# plot time vs height, height with moving average and phaseshifted height
plot_2d(columns[0], columns[4], columns[0], columns_ma[4], x_phase_height, y_phase_height, title="Height",
        x_axis=headers[0], y_axis=headers[4], legend_a="Height", legend_b="Height with moving average",
        legend_c="Height phase shifted")
