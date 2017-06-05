module WangMatrix
  class MazeGenerator
    attr_reader :grid, :smallest_x, :smallest_y

    def initialize(grid:, smallest_x: 4, smallest_y: 3)
      @grid = grid
      @smallest_x = smallest_x
      @smallest_y = smallest_y
    end

    def perform
      generate(x: 0, y:0, w: grid.width-1, h: grid.height-1, cut_vertical: true, depth: 1)
      grid.setxy(1, 0, Tile.start(pos: Pos.new(1,0), visible: true))
      grid.setxy(grid.width-2, grid.height-1, Tile.end(pos: Pos.new(grid.width-2, grid.height-1), visible: true))
      grid.setxy(1, 1, Tile.wall(pos: Pos.new(1,1)))
      grid.setxy(2, 1, Tile.wall(pos: Pos.new(1,1)))
      grid.setxy(3, 1, Tile.wall(pos: Pos.new(1,1)))
    end


    private

      #NOTE: depth is here purely for debugging
      def generate(x:, y:, w: grid.width-1, h: grid.height-1, cut_vertical: true, depth: 1)
        #puts grid.to_s
        #puts "x: #{x}, y: #{y}, w: #{w}, h: #{h}, vert: #{cut_vertical}, depth: #{depth}\n\n"

        if cut_vertical

          x_cut = x + rand(w)
          w_left = x_cut - x
          w_right = x + w - x_cut

          unless w_left < smallest_x || w_right < smallest_x
            0.upto(h-1) do |delta|
              grid.setxy(x_cut, y+delta, Tile.wall(pos: Pos.new(x_cut, y+delta), visible: true))
            end

            door_y = y+rand(h-1)+1
            grid.setxy(x_cut, door_y, Tile.space(pos: Pos.new(x_cut, door_y), visible: true))

            generate(x: x,     y: y, w: w_left,  h: h, cut_vertical: false, depth: depth+1)
            generate(x: x_cut, y: y, w: w_right, h: h, cut_vertical: false, depth: depth+1)
          end
        else

          y_cut = y + rand(h)
          h_top = y_cut - y
          h_bottom = h + y - y_cut

          unless h_top < smallest_y || h_bottom < smallest_y
            0.upto(w-1) do |delta|
              grid.setxy(x+delta, y_cut, Tile.wall(pos: Pos.new(x+delta, y_cut), visible: true))
            end

            door_x = x+rand(w-1)+1
            grid.setxy(door_x, y_cut, Tile.space(pos: Pos.new(x_cut, door_y), visible: true))

            generate(x: x, y: y,     w: w, h: h_top,    cut_vertical: true, depth: depth+1)
            generate(x: x, y: y_cut, w: w, h: h_bottom, cut_vertical: true, depth: depth+1)
          end
        end
      end
  end
end
