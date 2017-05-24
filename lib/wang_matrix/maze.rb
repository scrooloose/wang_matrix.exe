module WangMatrix
  class Maze
    attr_reader :maze_start, :maze_end

    def initialize(grid:, maze_start:, maze_end:)
      @grid = grid
      @maze_start = maze_start
      @maze_end = maze_end
    end

    def at(pos)
      grid[pos.y][pos.x]
    end

    def traversable?(pos)
      ['e', ' '].include?(at(pos))
    end

    def finish?(pos)
      at(pos) == "e"
    end

    def adjacent(pos)
      rv = []

      rv << pos.up unless pos.y <= 0
      rv << pos.down unless pos.y >= height-1
      rv << pos.left unless pos.x <= 0
      rv << pos.right unless pos.x >= width-1

      rv.select {|p| traversable?(p) }
    end

    def to_grid
      #deep clone hack
      Marshal.load(Marshal::dump(grid))
    end

    private
      attr_reader :grid

      def height
        @height ||= grid.size
      end

      def width
        @width ||= grid.first.size
      end
  end
end
