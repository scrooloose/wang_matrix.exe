module WangMatrix
  class Engine
    attr_reader :maze, :player

    def initialize(maze:, player:)
      @maze = maze
      @player = player
      @done = false
    end

    def main_loop
      ui.setup

      maze.update_visibility_from(player.pos)

      while !@done
        ui.render
        handle_player_action(ui.get_player_action)
      end

    ensure
      ui.teardown
    end


    private

      def ui
        @ui ||= UI.new(maze: maze, player: player)
      end

      #FIXME: at some point need a proper PlayerAction class or anything better
      #than this. An observer or similar would be good too.
      #
      #Presently we know that `action` will be a symbol that matches method
      #names in Player - move_up, move_down etc
      def handle_player_action(action)
        player.send(action)
      rescue
        @done = true
      end
  end
end
