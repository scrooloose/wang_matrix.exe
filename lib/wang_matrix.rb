require 'ncurses'
require 'forwardable'
require 'ostruct'
require 'logger'

require_relative "wang_matrix/maze"
require_relative "wang_matrix/maze_file_parser"
require_relative "wang_matrix/pos"
require_relative "wang_matrix/renderer/base"
require_relative "wang_matrix/renderer/null"
require_relative "wang_matrix/renderer/ncurses_renderer"
require_relative "wang_matrix/solver"
require_relative "wang_matrix/engine"
require_relative "wang_matrix/player"
require_relative "wang_matrix/ui"
require_relative "wang_matrix/grid"
require_relative "wang_matrix/maze_generator"
require_relative "wang_matrix/tile"

Log = Logger.new(File.dirname(__FILE__) + "/../log/log.log")
