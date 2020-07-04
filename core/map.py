class Map:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.__grid = []

        self.clear()

    def clear(self):
        self.__grid = [False] * (self.columns * self.rows)

    def cell_at_index(self, index):
        return self.__grid[index]

    def cell_at(self, x, y):
        return self.__grid[y * self.columns + x]

    def toggle_cell_at(self, x, y):
        self.__grid[y * self.columns + x] = not self.cell_at(x, y)

    def step(self):
        def gci(x, y):
            if x >= self.columns or x < 0 or y >= self.rows or y < 0:
                return 0
            else:
                return int(self.__grid[y * self.columns + x])

        def count_neighbours(x, y):
            return sum(map(lambda offset: gci(x + offset[0], y + offset[1]), [
                (-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)
            ]))

        new_grid = [False] * (self.columns * self.rows)

        for i in range(self.columns):
            for j in range(self.rows):
                alive = self.cell_at(i, j)
                count = count_neighbours(i, j)

                if ((count == 2 or count == 3) and alive) or (count == 3 and not alive):
                    new_grid[j * self.columns + i] = True

        self.__grid = new_grid
