module WangMatrix
  class Player
    extend Forwardable
    def_delegators :@pos, :x, :y

    attr_reader :pos, :maze

    def initialize(pos:, maze:)
      @pos = pos
      @maze = maze
    end

    def move_up
      move_to(pos.up)
    end

    def move_down
      move_to(pos.down)
    end

    def move_left
      move_to(pos.left)
    end

    def move_right
      move_to(pos.right)
    end

    private

      attr_writer :pos

      def move_to(pos)
        self.pos = pos if maze.traversable?(pos)
      end
  end
end
