module WangMatrix
  class MazeFileParser
    def perform(fname)
      grid = File.readlines(fname).
        map {|l| l.sub("\n", '')}.
        map {|l| l.split(//)}

      Maze.new(
        grid: grid,
        maze_start: find_in_grid(grid: grid, char: 's'),
        maze_end: find_in_grid(grid: grid, char: 'e')
      )
    end

    private

      def find_in_grid(grid:, char:)
        grid.each_with_index do |line, y|
          line.each_with_index do |c, x|
            if c == char
              return Pos.new(x, y)
            end
          end
        end
      end
  end
end
