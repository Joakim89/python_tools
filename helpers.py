import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import LinearAxis, Range1d


#########################################################
# writing
#########################################################

# Writes a list of arrays to a file. All arrays in "arrays" must be same length
# E.g. two arrays [[1, 2, 3], [a, b, c]], with ";" as delimiter will print:
#   1;a
#   2;b
#   3;c
def write_arrays_to_file(arrays, file_name, delimiter=";"):
    f = open(file_name, "w")
    for i in range(0, len(arrays[0])):
        s = ""
        for j in range(0, len(arrays)):
            s += str(arrays[j][i]) + delimiter
        s = s[:-1]
        f.write(s + "\n")


#########################################################
# reading
#########################################################

# Helping method for reading, strings to float.
# "," will be replaced with ".", and "" or "NAN" will be converted to zero.
def str_to_float(s):
    num = 0.0
    s = s.strip()
    s = s.replace(",", ".")
    if s != "" and s != "NAN":
        num = float(s)
    return num


# read columns from a PGHW Export file(txt-file generated from a PGHW export)
# parameters:
#   - file_name: file destination for the pg2 file.
#   - column_positions: default reads all columns in txt file. If not default, it reads only the column numbers
#     from column_positions. e.g. column_positions[0,2] it will read the first and third column.
# Returns:
#   1. A header list, containing the names of the columns
#   2. A list of columns, containing the data from the columns
# OBS: "," will be replaced with ".", and "" or "NAN" will be converted to zero.
def read_PGHW_export(file_name, column_positions=[], delimiter=","):
    f = open(file_name, "r")
    while True:
        if f.readline().strip() == "Data:":
            break
    all_headers = f.readline().split(delimiter)
    if not column_positions:
        for i in range(0, len(all_headers)):
            column_positions.append(i)

    headers = []
    columns = []
    for i in range(0, len(column_positions)):
        columns.append([])
        headers.append(all_headers[column_positions[i]])

    for line in f:
        s = line.split(delimiter)
        for i in range(0, len(columns)):
            columns[i].append(str_to_float(s[column_positions[i]]))

    return headers, columns


#########################################################
# plotting
#########################################################

# Takes a list of arrays and plots them in one plot. x-values will just be [0, 1, 2, 3..]
def plot_1d(ys, title="1d plot"):
    xs = [[], [], [], [], [], [], [], [], [], [], [], []]
    colors = ["black", "blue", "purple", "green", "yellow", "red", "orange", "cyan", "chocolate", "deeppink", "salmon", "olive"]
    for i in range(0, len(ys)):
        for j in range(0, len(ys[i])):
            xs[i].append(j)

    p = figure(sizing_mode='stretch_both', title=title)

    for i in range(0, len(ys)):
        p.line(xs[i], ys[i], line_width=1, legend=str(i), color=colors[i])

    show(p)


# Plot up to 3 x,y coordinate sets in the same plot.
def plot_2d(x_1, y_1, x_2=[], y_2=[], x_3=[], y_3=[], title="2d plot", legend_a="a", legend_b="b", legend_c="c", x_axis="x", y_axis="y"):
    p = figure(sizing_mode='stretch_both', title=title, x_axis_label=x_axis, y_axis_label=y_axis)

    p.line(x_1, y_1, line_width=1, legend=legend_a, color="black")
    if len(x_2) > 0:
        p.line(x_2, y_2, line_width=1, legend=legend_b, color="red")
    if len(x_3) > 0:
        p.line(x_3, y_3, line_width=1, legend=legend_c, color="blue")
    show(p)


# plot up to 12 x,y coordinate sets in one plot. First parameter is a list of x-coordinate arrays, next is a list of
# y-coordinate sets.
def plot_2d_many(xs, ys, title="2d plot", x_axis="x", y_axis="y", a_circle=False, v_line_pos=-1):
    p = figure(sizing_mode='stretch_both', title=title, x_axis_label=x_axis, y_axis_label=y_axis)
    colors = ["black", "blue", "purple", "green", "yellow", "red", "orange", "cyan", "chocolate", "deeppink", "salmon", "olive"]

    for i in range(0, len(ys)):
        p.line(xs[i], ys[i], line_width=1, legend=str(i), color=colors[i])

    show(p)


# plot 2 x,y coordinate sets on the same plot, but with separate y-axes.
def plot_2_y_axis(x_1, y_1, x_2, y_2, legend_a="a", legend_b="b", x_axis="x", y_axis_1="y1", y_axis_2="y2", title="Chart title"):
    p = figure(sizing_mode='stretch_both', x_axis_label=x_axis, y_axis_label=y_axis_1, title=title)
    second_axis_name = "2nd_y_axis"
    y1_min, y1_max, y2_min, y2_max = min(y_1), max(y_1), min(y_2), max(y_2)
    overlimit_factor = 0.01
    y1_overlimit, y2_overlimit = (y1_max-y1_min)*overlimit_factor, (y2_max-y2_min)*overlimit_factor
    y1_axis_start, y1_axis_end = y1_min-y1_overlimit, y1_max+y1_overlimit
    y2_axis_start, y2_axis_end = y2_min-y2_overlimit, y2_max+y2_overlimit

    # first axis
    p.line(x_1, y_1, legend=legend_a, color="blue")
    p.y_range = Range1d(y1_axis_start, y1_axis_end)

    # second axis
    p.extra_y_ranges = {second_axis_name: Range1d(y2_axis_start, y2_axis_end)}
    p.add_layout(LinearAxis(y_range_name=second_axis_name, axis_label=y_axis_2), "right")
    p.line(x_2, y_2, y_range_name=second_axis_name, legend=legend_b, color="red")
    show(p)


#########################################################
# filtering
#########################################################

# will change even length to uneven, by adding 1
# simple moving average function. Takes a list of numbers y, and returns a list, with the same length, of the
# moving average with the length specified. Zeros are added at the start and end, where there's not enough numbers to
# calculate the moving average.
def moving_avg_fast(y, length):
    if length % 2 == 0:
        length += 1
    sm_x = (np.cumsum(y) - np.cumsum(np.concatenate((np.zeros(length), y[:-length])))) / length
    return np.concatenate((np.zeros(int(length/2)), sm_x[int(length-1):], np.zeros(int(length / 2))))


# Moving average, but high-pass. Meaning this will subtract your original data with a moving average, resulting in a
# simple high pass filter. Zeros are added at the start and end, where there's not enough numbers to calculate the
# moving average.
def high_pass_ma(y, length):
    acc_lp = []
    acc_lp[:] = y
    acc_lp = moving_avg_fast(acc_lp, length)
    return list(np.array(y) - np.array(acc_lp))


#########################################################
# Graphs
#########################################################

# Get a sine curve, to match an input x list.
# Personalize your sine curve by adjusting parameters, freq, amp and phase.
def get_sine(x, freq=1, amp=1, phase=0):
    sine = []
    for t in x:
        sine.append(amp*np.sin(2*np.pi*freq*t+phase))
    return sine


# Returns a square wave, to match an input x list. Goes up and down symmetrically around 0.
# Starts up if phase=0 (default). Choose amplitude, frequency and phase.
# Use dc to move graph up or down
def get_square_wave(x, freq=1, amp=1, phase=0, dc=0):
    wave = []
    wl = 1/freq
    for t in x:
        res = (t-phase) % wl
        if res < wl/2:
            wave.append(amp+dc)
        else:
            wave.append(-amp+dc)
    return wave


# Returns y-values for a time series x, corresponding to a straight line, with the equation y=ax+b
def get_straight_line(x, a=1, b=0):
    y = []
    for t in x:
        y.append(a*t+b)
    return y


# Takes a x,y coordinate set as input, and returns the corresponding linear regression.
# Input: x and y values (must be same length)
# Returns: a and b in y=ax+b
def linear_regression(x, y):
    n = len(x)
    sum_x, sum_y, sum_x_sqr, sum_xy = 0, 0, 0, 0
    for i in range(0, n):
        sum_x += x[i]
        sum_y += y[i]
        sum_x_sqr += x[i]**2
        sum_xy += x[i]*y[i]

    a = (n*sum_xy - sum_x*sum_y) / (n*sum_x_sqr - sum_x**2)
    b = (sum_y - a*sum_x) / n

    return a, b


#########################################################
# numerical operations
#########################################################

# OBS: Only works on equidistant data
# Phase shift your data in either direction.
# Parameters:
#   x, y: A coordinate set. Both lists must be the same length.
#   phase: number of points you want to shift the data. Sign determines the direction.
#   default_value: Value of inserted points at the start or end of the data (depending on the direction of the phase
#   shift).
# Returns:
#   An x,y coordinate set with the same length as the input.
def phase_shift(x, y, phase, default_value=0.0):
    x_out, y_out = [], []
    if phase >= 0:
        for i in range(0, phase):
            x_out.append(x[i])
            y_out.append(default_value)
        for i in range(phase, len(x)):
            x_out.append(x[i])
            y_out.append(y[i-phase])
    else:
        phase = abs(phase)
        for i in range(0, len(x)-phase):
            x_out.append(x[i])
            y_out.append(y[i+phase])
        for i in range(len(x)-phase, len(x)):
            x_out.append(x[i])
            y_out.append(default_value)
    return x_out, y_out


# Takes a list of lists and cuts the length of the lists to match the length of the shortest list.
# The values in the end of the list are cut.
def cut_to_shortest_length(lists):
    min_length = -1
    for arr in lists:
        if len(arr) < min_length or min_length == -1:
            min_length = len(arr)
    for arr in lists:
        arr[:] = arr[0:min_length]
