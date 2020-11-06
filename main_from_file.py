from plotter import Plotter

##Import code from FUNCTION/CLASS file here

## READ list of x,y coordinates from POLGYON.CSV as poly_points (list)

with open('polygon.csv', 'r') as f:
    data = f.readlines()[1:] #skip header
    poly_points = []
    poly_x = []
    poly_y = []
    for line in data:
        res = line.rstrip().split(',')[1:] #split by line
        res = [float(i) for i in res] #convert to integers
        poly_points.append(res)
    poly_x = [i[0] for i in poly_points]
    poly_y = [i[1] for i in poly_points]
print(poly_points)
print(poly_x)
print(poly_y)

with open('input.csv', 'r') as f:
    data = f.readlines()[1:] #skip header
    input_points = []
    input_x = []
    input_y = []
    for line in data:
        res = line.rstrip().split(',')[1:] #split by line
        res = [float(i) for i in res] #convert to integers
        input_points.append(res)
    input_x = [i[0] for i in input_points]
    input_y = [i[1] for i in input_points]
print(input_points)
print(input_x)
print(input_y)

plotter = Plotter()
plotter.add_polygon(poly_x, poly_y)
plotter.add_point(input_x, input_y)
plotter.show()

## Create a polygon OBJECT from poly_points in clockwise order as polygon_obj (obj)
## READ list of x,y coordinates from INPUT.CSV as input_points (list)

# CATEGORISE input_points as inside, outside or boundary and save to category_result (list)

# WRITE the category_result to a CSV file

# PLOT the points and polygon in a plot window

def main():
    plotter = Plotter()
    print("read polygon.csv")

    print("read input.csv")

    print("categorize points")

    print("write output.csv")

    print("plot polygon and points")
    #plotter.show()

##Put your solution here ^^^

if __name__ == "__main__":
    main()

