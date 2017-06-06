module WangMatrix
  class Tile
    attr_reader :pos, :char

    attr_writer :visible

    def initialize(pos:, char:, transparent:, traversable:, visible: false)
      @pos = pos
      @char = char
      @transparent = transparent
      @traversable = traversable
      @visible = visible
    end

    def self.space(pos:, **args)
      new({pos: pos, transparent: true, traversable: true, char: " "}.merge(args))
    end

    def self.wall(pos:, **args)
      new({pos: pos, transparent: false, traversable: false, char: "#"}.merge(args))
    end

    def self.start(pos:, **args)
      new({pos: pos, transparent: false, traversable: false, char: "s"}.merge(args))
    end

    def self.end(pos:, **args)
      new({pos: pos, transparent: false, traversable: true, char: "e"}.merge(args))
    end

    def traversable?
      @traversable
    end

    def transparent?
      @traversable
    end

    def visible?
      @visible
    end

    def to_s
      "'#{char}' (#{pos.x},#{pos.y}) v:#{!!visible?}"
    end

    def inspect
      to_s
    end
  end
end
