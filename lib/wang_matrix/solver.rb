module WangMatrix
  class Solver

    def initialize(maze:, renderer: Renderer::Ncurses.new)
      @maze = maze
      @traversed = []
      @solution = []
      @renderer = renderer
    end

    def perform
      if perform_for_real
        solution.reverse!.unshift(maze.maze_start)
        renderer.present_solution(grid: maze.to_grid, path: solution)
      end
      solution
    ensure
      renderer.reset_screen
    end

    private

      attr_reader :renderer, :solution, :maze, :traversed

      def perform_for_real(current: maze.maze_start, path: [])
        renderer.perform(grid: maze.to_grid, path: path + [current])

        return true if maze.finish?(current)

        traversed << current

        adjacent(current).each do |a|
          if perform_for_real(current: a, path: path + [current])
            solution << a
            return true
          end
        end

        false
      end

      def adjacent(pos)
        maze.adjacent(pos).reject {|p| traversed.include?(p)}
      end
  end
end
