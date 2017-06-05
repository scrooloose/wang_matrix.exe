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

    def update_visibility_from(pos)
      grid.each do |tile|
        next if tile.visible?

        tile.visible = positions_have_los(pos, tile.pos)
      end
    end

    private
      attr_reader :grid

      def positions_have_los(p1, p2)
        between = p1.points_between(p2)

        return true if between.empty?

        between.all? do |p|
          grid.at(p).transparent?
        end
      end
  end
end
