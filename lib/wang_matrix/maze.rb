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

      rv << Pos.new(pos.x,   pos.y-1)
      rv << Pos.new(pos.x,   pos.y+1)
      rv << Pos.new(pos.x-1, pos.y)
      rv << Pos.new(pos.x+1, pos.y)

      rv.select {|p| traversable?(p) }
    end

    def to_grid
      #deep clone hack
      Marshal.load(Marshal::dump(grid))
    end

    private
      attr_reader :grid
  end
end
