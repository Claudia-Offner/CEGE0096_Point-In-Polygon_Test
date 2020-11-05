from plotter import Plotter


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
