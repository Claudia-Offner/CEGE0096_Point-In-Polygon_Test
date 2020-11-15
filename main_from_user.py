from plotter import Plotter
from pip import Point, Polygon, Square
""" The plotter module will be used to plot data """
""" The pip module will be used to run MBR and RCA algorithms """


def csv_reader(path):
    """ Reads csv files line by line as a nested list of floats """

    with open(path, 'r') as f:
        data = f.readlines()[1:]
        points = []
        for line in data:
            res = line.rstrip().split(',')
            res = [float(i) for i in res]
            points.append(res)
        return points


def csv_writer(file):
    """ Writes nested lists into csv files as strings """

    header = ['id', 'category']
    with open('original_output.csv', 'w') as f:
        f.write(str(header).translate({39: None})[1:-1] + '\n')
        for line in file:
            f.write(str(line).translate({39: None})[1:-1] + '\n')


def transpose_matrix(matrix):
    """ Transpose matrix for nested lists """

    res = []
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    for r in result:
        res.append(r)
    return res


def main():
    """ Point in Polygon Test """

    # Read data for analysis
    poly_list = csv_reader('polygon.csv')
    print('Read polygon.csv: ', poly_list)

    # Extract X's and Y's for plotter inputs
    poly_x = [i[1] for i in poly_list]
    poly_y = [i[2] for i in poly_list]

    # Get user inputs
    print('Insert point information')
    x1 = float(input('x coordinate: '))
    y1 = float(input('y coordinate: '))

    print("Insert point information")
    x2 = float(input('x coordinate: '))
    y2 = float(input('y coordinate: '))

    # Convert polygon and inputs into Point objects
    poly_p = []
    for i in poly_list:
        point = Point(i[0], i[1], i[2])
        poly_p.append(point)
    input_p = [Point(1, x1, y1), Point(2, x2, y2)]

    # Create Plotter Object (plotter), Square Object (s) and Polygon Object (p)
    plotter = Plotter()
    s = Square([point for point in poly_p])
    p = Polygon([point for point in poly_p])

    # GET MBR RESULTS #

    # Extract MBR outputs
    mbr_id = [i.name for i in input_p]
    mbr_x = [i.x for i in input_p]
    mbr_y = [i.y for i in input_p]
    mbr_out = [s.get_mbr(i) for i in input_p]
    mbr_out = [item for i in mbr_out for item in i]
    mbr_res = transpose_matrix([mbr_id, mbr_x, mbr_y, mbr_out])
    print('MBR Results: ', mbr_res)

    # Separate points inside & outside MBR
    mbr_in = []
    mbr_out = []
    for i in mbr_res:
        if i[3] == 'inside':
            mbr_in.append(i)
        else:
            mbr_out.append(i)
            continue

    # Create Point object for points inside mbr (for boundary analysis)
    in_mbr = []
    for i in mbr_in:
        point = Point(i[0], i[1], i[2])
        in_mbr.append(point)

    # GET BOUNDARY RESULTS #

    # Extract Boundary outputs from points inside mbr
    bound_id = [i.name for i in in_mbr]
    bound_x = [i.x for i in in_mbr]
    bound_y = [i.y for i in in_mbr]
    bound_out = [p.bound(i) for i in in_mbr]

    # Categorise points on/off polygon boundaries
    bound_res = []
    for i in bound_out:
        if i is True:
            bound_res.append('boundary')
        else:
            bound_res.append('n/a')
    bound_res = transpose_matrix([bound_id, bound_x, bound_y, bound_res])

    # Categorise vertices as on boundary
    vertex_on = []
    for i in bound_res:
        for j in poly_list:
            if i[1] == j[1] and i[2] == j[2]:
                vertex_on.append(i)
    for i in vertex_on:
        i[3] = 'boundary'

    # Replace vertex values with the correct category
    for i in bound_res:
        for j in vertex_on:
            if i[0] == j[0]:
                i = j
    print('Boundary Results: ', bound_res)

    # Separate points that are on and off the boundary
    bound_on = []
    bound_off = []
    for i in bound_res:
        if i[3] == 'boundary':
            bound_on.append(i)
        else:
            bound_off.append(i)
            continue

    # Create Point object for points not on boundary (for RCA analysis)
    off_bound = []
    for i in bound_off:
        point = Point(i[0], i[1], i[2])
        off_bound.append(point)

    # GET RCA RESULTS #

    # Extract RCA outputs from points not on the boundary and inside the mbr
    rca_id = [i.name for i in off_bound]
    rca_x = [i.x for i in off_bound]
    rca_y = [i.y for i in off_bound]
    rca_out = [p.contains(i) for i in off_bound]
    rca_res = []
    for i in rca_out:
        if i is True:
            rca_res.append('inside')
        else:
            rca_res.append('outside')
    rca_res = transpose_matrix([rca_id, rca_x, rca_y, rca_res])
    print('RCA Results: ', rca_res)

    # Separate points that are inside and outside RCA
    rca_in = []
    rca_out = []
    for i in rca_res:
        if i[3] == 'inside':
            rca_in.append(i)
        else:
            rca_out.append(i)
            continue

    # CATEGORISE DATA OUTPUTS #

    # Combine points outside the RCA with points outside the MBR
    for i in rca_out:
        mbr_out.append(i)

    # Categorise points
    final = []
    for p in input_p:
        for i in mbr_out:
            if p.name == i[0]:
                final.append(i)
            else:
                continue
        for i in bound_on:
            if p.name == i[0]:
                final.append(i)
            else:
                continue
        for i in rca_in:
            if p.name == i[0]:
                final.append(i)

    final_plot = transpose_matrix(final)

    print('Categorize points: ', final)

    # PLOT POINTS #

    # Optimise category outputs for file export
    write_output = transpose_matrix([[int(i) for i in final_plot[0]], final_plot[3]])
    csv_writer(write_output)

    print('Write output.csv: ', write_output)

    # Plot Plot final results
    plotter.add_polygon(poly_x, poly_y)
    for x, y, label in zip(final_plot[1], final_plot[2], final_plot[3]):
        plotter.add_point(x, y, kind=label)
    plotter.add_label('X-axis', 'Y-axis', 'Point in Polygon Test')
    plotter.show()


if __name__ == '__main__':
    main()