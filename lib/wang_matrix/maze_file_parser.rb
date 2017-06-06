module WangMatrix
  class MazeFileParser
    def perform(fname)
      lines = File.readlines(fname)

      tiles = []

      lines.each_with_index.map do |line, y|
        line.sub("\n", '').split('').each_with_index.map do |char, x|
          tiles << tile_for(char: char, x: x, y: y)
        end
      end

      grid = Grid.new_from_array(tiles)

      Maze.new(
        grid: grid,
        maze_start: grid.find('s').pos,
        maze_end: grid.find('e').pos
      )
    end

    private

      def tile_for(char:, x:, y:)
        pos = Pos.new(x, y)

        case char
        when "#" then Tile.wall(pos: pos)
        when "s" then Tile.start(pos: pos)
        when "e" then Tile.end(pos: pos)
        when " " then Tile.space(pos: pos)
        else
          raise "Unexpected char '#{char}'"
        end
      end
  end
end
