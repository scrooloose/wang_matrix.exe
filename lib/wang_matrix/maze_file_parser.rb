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
        maze_start: grid.find('s'),
        maze_end: grid.find('e')
      )
    end

    private

      def tile_for(char:, x:, y:)
        pos = Pos.new(x, y)

        case char
        when "#" then Tile.new(pos: pos, char: char, traversable: false, transparent: false)
        when "s" then Tile.new(pos: pos, char: char, traversable: true, transparent: true)
        when "e" then Tile.new(pos: pos, char: char, traversable: true, transparent: true)
        when " " then Tile.new(pos: pos, char: char, traversable: true, transparent: true)
        else
          raise "Unexpected char '#{char}'"
        end
      end
  end
end
