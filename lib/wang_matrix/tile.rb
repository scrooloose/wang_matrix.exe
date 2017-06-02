module WangMatrix
  class Tile
    attr_reader :pos, :char

    def initialize(pos:, char:, transparent:, traversable:, visible: false)
      @pos = pos
      @char = char
      @transparent = transparent
      @traversable = traversable
      @visible = visible
    end

    def traversable?
      @traversable
    end

    def transparent?
      @traversable
    end

    def visible?
      @traversable
    end

    def to_s
      "'#{char}' (#{pos.x},#{pos.y})"
    end

    def inspect
      to_s
    end
  end
end
