from plotter import Plotter

##Import code from FUNCTION/CLASS file here (alter for user inputs)

## READ list of x,y coordinates from POLGYON.CSV as poly_points (list)
## Create a polygon OBJECT from poly_points in clockwise order as polygon_obj (obj)
# READ a point from a user for testing

# CATEGORISE input_points as inside, outside or boundary and save to category_result (list)

# PLOT the points and polygon in a plot window


def main():
    plotter = Plotter()
    print("read polygon.csv")

    print("Insert point information")
    x = float(input("x coordinate: "))
    y = float(input("y coordinate: "))

    print("categorize point")

    print("plot polygon and point")
    plotter.show()


if __name__ == "__main__":
    main()


