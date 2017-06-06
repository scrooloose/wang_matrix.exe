module WangMatrix
  class Grid
    attr_reader :width, :height
    def initialize(width: 5, height: 5)
      @grid = (0..(height-1)).map { Array.new(width) }
      @width = width
      @height = height
      init_with_spaces
    end

    def self.new_from_array(array)
      height = array.max {|obj| obj.pos.y}.pos.y+1
      width = array.max {|obj| obj.pos.x}.pos.x+1
      grid = new(width: width, height: height)

      array.each {|obj| grid.set(obj)}
      grid
    end

    def at(pos)
      atxy(pos.x, pos.y)
    end

    def atxy(x, y)
      grid[y][x]
    end

    def set(positionable)
      pos = positionable.pos
      raise "Invalid x (#{pos.x}). Width: #{width}" if pos.x >= width
      raise "Invalid y (#{pos.y}). Height #{height}" if pos.y >= height
      grid[pos.y][pos.x] = positionable
    end

    def find(tile_char)
      grid.each_with_index do |line, y|
        line.each_with_index do |tile, x|
          return tile if tile && tile.char == tile_char
        end
      end
    end

    def clone
      #deep clone hack
      Marshal.load(Marshal::dump(self))
    end

    def to_s(force_visible: false)
      grid.map do |line|
        line.map do |tile|
          if tile.visible? || force_visible
            tile.char
          else
            " "
          end
        end.join
      end.join("\n")
    end

    def each
      grid.each_with_index do |line, y|
        line.each_with_index do |tile, x|
          yield tile
        end
      end
    end

    private
      attr_reader :grid

      def init_with_spaces
        grid.each_with_index do |line, y|
          line.each_with_index do |tile, x|
            set(Tile.space(pos: Pos.new(x, y)))
          end
        end
        self
      end
  end
end
