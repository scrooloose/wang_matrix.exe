module WangMatrix
  class UI
    attr_accessor :maze, :player

    def initialize(maze:, player:)
      @maze = maze
      @player = player
    end

    def setup
      Ncurses.initscr
      Ncurses.start_color
      Ncurses.cbreak
      Ncurses.curs_set(0)
      Ncurses.init_pair(1, Ncurses::COLOR_WHITE, Ncurses::COLOR_BLACK)
      Ncurses.init_pair(2, Ncurses::COLOR_YELLOW, Ncurses::COLOR_BLACK)
      screen.keypad(true)
    end

    def teardown
      # put the screen back in its normal state
      Ncurses.echo()
      Ncurses.nocbreak()
      Ncurses.nl()
      Ncurses.endwin()
      Ncurses.curs_set(1)
    end

    def render
      grid = maze.to_grid
      screen.clear
      screen.attrset(Ncurses::COLOR_PAIR(1))
      screen.mvaddstr(0,0, grid.to_s + "\n\n")

      screen.attrset(Ncurses::COLOR_PAIR(2))
      screen.mvaddstr(player.y, player.x, "@")

      screen.refresh
    end

    def get_player_action
      case screen.getch
      when Ncurses::KEY_UP then :move_up
      when Ncurses::KEY_DOWN then :move_down
      when Ncurses::KEY_LEFT then :move_left
      when Ncurses::KEY_RIGHT then :move_right
      end
    end

    private

      def screen
        Ncurses.stdscr
      end
  end
end
