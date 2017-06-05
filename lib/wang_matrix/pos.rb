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

    def points_between(other)
      line_to(other).reject {|p| p == other || p == self}
    end

    private

      #Use Bresenham's line alg. Stolen + adapted from
      #https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Ruby
      def line_to(p)
        x1, y1 = self.x, self.y
        x2, y2 = p.x, p.y

        steep = (y2 - y1).abs > (x2 - x1).abs

        if steep
          x1, y1 = y1, x1
          x2, y2 = y2, x2
        end

        if x1 > x2
          x1, x2 = x2, x1
          y1, y2 = y2, y1
        end

        deltax = x2 - x1
        deltay = (y2 - y1).abs
        error = deltax / 2
        ystep = y1 < y2 ? 1 : -1

        rv = []

        y = y1
        x1.upto(x2) do |x|
          rv << if steep
                  self.class.new(y,x)
                else
                  self.class.new(x,y)
                end

          error -= deltay
          if error < 0
            y += ystep
            error += deltax
          end
        end

        rv.first == self ? rv : rv.reverse
      end
  end
end
