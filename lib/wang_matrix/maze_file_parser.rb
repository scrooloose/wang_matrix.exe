module WangMatrix
  class MazeFileParser
    def perform(fname)
      raw_grid = File.readlines(fname).
        map {|l| l.sub("\n", '')}.
        map {|l| l.split(//)}

      grid = Grid.from_2d_array(raw_grid)

      Maze.new(
        grid: grid,
        maze_start: grid.find('s'),
        maze_end: grid.find('e')
      )
    end
  end
end
