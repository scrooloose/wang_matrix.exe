module WangMatrix
  class Solver
    attr_reader :maze, :traversed

    def initialize(maze:, renderer: Renderer::Ncurses.new)
      @maze = maze
      @traversed = []
      @renderer = renderer
    end

    def perform
      solution = perform_for_real
      renderer.present_solution(grid: maze.to_grid, path: solution)
    ensure
      renderer.reset_screen
    end

    private

      attr_reader :renderer

      def perform_for_real(current: maze.maze_start, path: [])
        renderer.perform(grid: maze.to_grid, path: path + [current])

        if maze.finish?(current)
          return path + [current]
        end

        traversed << current

        adjacent(current).each do |a|
          result = perform_for_real(current: a, path: path + [current])
          if result.any? && maze.finish?(result.last)
            return result
          end
        end
      end

      def adjacent(pos)
        maze.adjacent(pos).reject {|p| traversed.include?(p)}
      end
  end
end
