#!/usr/bin/env ruby

require_relative "../lib/wang_matrix"

g = WangMatrix::MazeGenerator.new(
  grid: WangMatrix::Grid.new(width: 150, height: 40).add_border,
  smallest_x: 4,
  smallest_y: 4
)
g.perform
puts g.grid
