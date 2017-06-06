module WangMatrix
  class Maze
    attr_reader :maze_start, :maze_end

    extend Forwardable
    def_delegators :@grid, :at, :atxy, :width, :height

    def initialize(grid:, maze_start:, maze_end:)
      @grid = grid
      @maze_start = maze_start
      @maze_end = maze_end
    end

    def traversable?(pos)
      at(pos)&.traversable?
    end

    def finish?(pos)
      pos == maze_end
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

    def update_visibility_from(pos, range: 10, workers: 8)
      start_x = [pos.x - range, 0].max
      start_y = [pos.y - range, 0].max
      final_x = [width-1, pos.x + range].min
      final_y = [height-1, pos.y + range].min

      results = Parallel.map((start_y..final_y).to_a, in_process: workers) do |y|
        start_x.upto(final_x).map do |x|
          tile = atxy(x, y)

          next if tile.visible?

          [x,y] if positions_have_los(pos, tile.pos)
        end.compact
      end

      results.flatten!(1)

      results.each do |coord|
        x,y = coord

        tile = atxy(x,y)
        tile.visible = true
      end

    end

    private
      attr_reader :grid

      def positions_have_los(p1, p2)
        between = p1.points_between(p2)

        return true if between.empty?

        between.none? do |p|
          !grid.at(p).transparent?
        end
      end
  end
end
