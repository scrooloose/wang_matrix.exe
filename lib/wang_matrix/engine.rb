module WangMatrix
  class Engine
    attr_reader :maze, :player

    def initialize(maze:, player:)
      @maze = maze
      @player = player
    end

    def main_loop
      init_ui

      loop do
        render
        handle_key_press(screen.getch)
      end

    ensure
      reset_screen
    end


    private

      def init_ui
        Ncurses.initscr
        Ncurses.start_color
        Ncurses.cbreak
        Ncurses.curs_set(0)
        Ncurses.init_pair(1, Ncurses::COLOR_WHITE, Ncurses::COLOR_BLACK)
        Ncurses.init_pair(2, Ncurses::COLOR_YELLOW, Ncurses::COLOR_BLACK)
        screen.keypad(true)
      end

      def screen
        Ncurses.stdscr
      end

      def reset_screen
        # put the screen back in its normal state
        Ncurses.echo()
        Ncurses.nocbreak()
        Ncurses.nl()
        Ncurses.endwin()
        Ncurses.curs_set(1)
      end

      def handle_key_press(key)
        case key
        when Ncurses::KEY_UP
          player.move_up
        when Ncurses::KEY_DOWN
          player.move_down
        when Ncurses::KEY_LEFT
          player.move_left
        when Ncurses::KEY_RIGHT
          player.move_right
        end
      end

      def render
        grid = maze.to_grid
        screen.clear
        screen.attrset(Ncurses::COLOR_PAIR(1))
        screen.mvaddstr(0,0, grid.map(&:join).join("\n") + "\n\n")

        screen.attrset(Ncurses::COLOR_PAIR(2))
        screen.mvaddstr(player.y, player.x, "@")

        screen.refresh
      end
  end
end
