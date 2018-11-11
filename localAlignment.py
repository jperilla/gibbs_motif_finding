import numpy as np


# This function returns "up", "left", "diag" for the direction
# to trace the path back through the DP table to get
# the best alignment
def get_direction(value, diag_value, up_value, left_value):
    if value == diag_value:
        return "D"

    if value == up_value:
        return "U"

    if value == left_value:
        return "L"

    return "N"


# Create alignment with local alignment algorithm
# This function fills the DP table with appropriate scores
# with a second table to show direction for printing
def create_alignment(v, w, gap, match, mismatch):
    # Initialize n and m, and a and b arrays
    n = len(v) + 1
    m = len(w) + 1
    a = np.zeros((n, m))
    b = np.chararray((n, m))
    print(b)
    sink = 0
    sink_coords = [0, 0]
    for i in range(1, n):
        for j in range(1, m):
            if v[i - 1] == w[j - 1]:
                # this is a match
                a[i, j] = max([0, a[i - 1, j] + gap, a[i, j - 1] + gap, a[i - 1, j - 1] + match])
                b[i, j] = get_direction(a[i, j], a[i - 1, j - 1] + match, a[i - 1, j] + gap, a[i, j - 1] + gap)
            else:  # not a match
                a[i, j] = max([0, a[i - 1, j] + gap, a[i, j - 1] + gap, a[i - 1, j - 1] + mismatch])
                b[i, j] = get_direction(a[i, j], a[i - 1, j - 1] + mismatch, a[i - 1, j] + gap, a[i, j - 1] + gap)

            # keep track of largest value for sink
            if a[i, j] > sink:
                sink = a[i, j]
                sink_coords = [i, j]

    return [a, b, sink, sink_coords[0], sink_coords[1]]


def print_alignment(b, v, w, i, j, score):
    f = open("output.txt", "w+")
    f.write("score = " + str(score) + "\r\n")
    v_align = ""
    w_align = ""

    while True:
        if i == 0 or j == 0:
            break

        print(b[i, j])
        if b[i, j] == b'D':
            print("D")
            v_align = v[i - 1] + v_align
            w_align = w[j - 1] + w_align
            i = i - 1
            j = j - 1
        elif b[i, j] == b'U':
            print("U")
            v_align = v[i - 1] + v_align
            w_align = "-" + w_align
            i = i - 1
        else:
            print("l")
            v_align = "-" + v_align
            w_align = w[j - 1] + w_align
            j = j - 1

    # output values to file
    f.write(v_align + "\r\n")
    f.write(w_align + "\r\n")
    f.close()


# Set v and w - > later you could read these in from a file
v = "GCTGGAAGGCAT"
w = "GCAGAGCACG"

# Set gap penalty (gap), match (match), mismatch (mismatch)
gap = -4
match = 5
mismatch = -4

dpTables = create_alignment(v, w, gap, match, mismatch)
print(dpTables)
dpValues = dpTables[0]
dpDirections = dpTables[1]
score = dpTables[2]
sink_i = dpTables[3]
sink_j = dpTables[4]

print_alignment(dpDirections, v, w, sink_i, sink_j, score)

