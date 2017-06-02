module WangMatrix
  class Maze
    attr_reader :maze_start, :maze_end

    extend Forwardable
    def_delegators :@grid, :at, :width, :height

    def initialize(grid:, maze_start:, maze_end:)
      @grid = grid
      @maze_start = maze_start
      @maze_end = maze_end
    end

    def at(pos)
      grid.at(pos)
    end

    def traversable?(pos)
      return false if pos.x >= width || pos.x < 0
      return false if pos.y >= height || pos.y < 0
      return at(pos).traversable?
    end

    def finish?(pos)
      at(pos).char == "e"
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
      grid.clone
    end

    private
      attr_reader :grid
  end
end
