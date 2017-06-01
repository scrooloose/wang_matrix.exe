module WangMatrix
  class Grid
    attr_reader :width, :height
    def initialize(width: 5, height: 5, default_fill: " ")
      @grid = (0..height).map { Array.new(width, default_fill) }
      @width = width
      @height = height
    end

    # @array: of horizontal lines
    def self.from_2d_array(array)
      new(width: array.first.size, height: array.size).tap do |grid|
        array.each_with_index do |line, y|
          line.each_with_index do |char, x|
            grid.setxy(x, y, array[y][x])
          end
        end
      end
    end

    def at(pos)
      grid[pos.y][pos.x]
    end

    def set(pos, char)
      setxy(pos.x, pos.y, char)
    end

    def setxy(x, y, char)
      raise "Invalid x (#{x}). Width: #{width}" if x >= width
      raise "Invalid y (#{y}). Height #{height}" if y >= height
      grid[y][x] = char
    end

    def find(char)
      grid.each_with_index do |line, y|
        line.each_with_index do |c, x|
          if c == char
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
      grid.map(&:join).join("\n")
    end

    def add_border(char: '#')
      0.upto(height-1) do |y|
        setxy(0, y, char)
        setxy(width-1, y, char)
      end

      0.upto(width-1) do |x|
        setxy(x, 0, char)
        setxy(x, height-1, char)
      end

      self
    end

    private
      attr_reader :grid

  end
end
