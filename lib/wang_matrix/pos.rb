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
  end
end
