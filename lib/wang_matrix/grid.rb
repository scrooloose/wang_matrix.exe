module WangMatrix
  class Grid
    attr_reader :width, :height
    def initialize(width: 5, height: 5)
      @grid = (0..(height-1)).map { Array.new(width-1) }
      @width = width
      @height = height
      init_with_spaces
    end

    # @array: of horizontal lines
    def self.from_2d_array(array)
      new(width: array.first.size, height: array.size).tap do |grid|
        array.each_with_index do |line, y|
          line.each_with_index do |obj, x|
            grid.setxy(x, y, array[y][x])
          end
        end
      end
    end

    def init_with_spaces
      grid.each_with_index do |line, y|
        line.each_with_index do |tile, x|
          setxy(x,y, Tile.space(pos: Pos.new(x, y)))
        end
      end
      self
    end

    def at(pos)
      grid[pos.y][pos.x]
    end

    def set(pos, obj)
      setxy(pos.x, pos.y, obj)
    end

    def setxy(x, y, obj)
      raise "Invalid x (#{x}). Width: #{width}" if x >= width
      raise "Invalid y (#{y}). Height #{height}" if y >= height
      grid[y][x] = obj
    end

    def find(tile_char)
      grid.each_with_index do |line, y|
        line.each_with_index do |tile, x|
          if tile.char == tile_char
            return Pos.new(x, y)
          end
        end
      end
    end

    def clone
      #deep clone hack
      Marshal.load(Marshal::dump(self))
    end

    def to_s
      grid.map do |line|
        line.map do |tile|
          if tile.visible?
            tile.char
          else
            " "
          end
        end.join
      end.join("\n")
    end

    def add_border(obj: '#')
      0.upto(height-1) do |y|
        setxy(0, y, Tile.wall(pos: Pos.new(0,y)))
        setxy(width-1, y, Tile.wall(pos: Pos.new(width-1,y)))
      end

      0.upto(width-1) do |x|
        setxy(x, 0, Tile.wall(pos: Pos.new(x,0)))
        setxy(x, height-1, Tile.wall(pos: Pos.new(x, height-1)))
      end

      self
    end

    def each(&block)
      grid.each_with_index do |line, y|
        line.each_with_index do |tile, x|
          yield tile
        end
      end
    end

    private
      attr_reader :grid

  end
end
