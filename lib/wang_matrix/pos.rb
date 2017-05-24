module WangMatrix
  class Pos
    attr_reader :x, :y
    def initialize(x, y)
      @x = x
      @y = y
    end

    def ==(p)
      [self.x, self.y] == [p.x, p.y]
    end

    def to_s
      inspect
    end

    def inspect
      "(#{x},#{y})"
    end

    def up
      Pos.new(x, y-1)
    end

    def down
      Pos.new(x, y+1)
    end

    def left
      Pos.new(x-1, y)
    end

    def right
      Pos.new(x+1, y)
    end
  end
end
