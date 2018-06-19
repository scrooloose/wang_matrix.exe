module WangMatrix
  RSpec.describe Maze do
    let(:grid) do
      Grid.new(width: 2, height: 2).tap do |g|
        g.set(Tile.floor(pos: Pos.new(0,0)))
        g.set(Tile.wall(pos: Pos.new(1,1)))
      end
    end
    subject { Maze.new(grid: grid, maze_start: Pos.new(0, 0), maze_end: Pos.new(1, 1)) }

    describe "#traversable?" do
      it "is true for traversable tiles" do
        expect(subject.traversable?(Pos.new(0, 0))).to be
      end

      it "is false for non traversable tiles" do
        expect(subject.traversable?(Pos.new(1, 1))).to_not be
      end
    end

    describe "#finish?" do
      it "is true for the finishing tile" do
        expect(subject.finish?(Pos.new(1, 1))).to be
      end

      it "is false for non finishing tiles" do
        expect(subject.finish?(Pos.new(0, 0))).to_not be
      end
    end

    describe "#adjacent" do
      it "returns traversable adjacent positions" do
        expect(subject.adjacent(Pos.new(1, 0))).to match_array(
          [Pos.new(0, 0)] #doesnt include wall at 1,1
        )
      end
    end

    describe "#update_visibility_from" do
      let(:grid) do

        #maze looks like:
        #  s##
        #  # #
        #  ##e
        Grid.new(width: 3, height: 3).tap do |g|
          g.set(Tile.start(pos: Pos.new(0, 0)))
          g.set(Tile.wall(pos: Pos.new(1, 0)))
          g.set(Tile.wall(pos: Pos.new(2, 0)))

          g.set(Tile.wall(pos: Pos.new(0, 1)))
          g.set(Tile.floor(pos: Pos.new(1, 1)))
          g.set(Tile.wall(pos: Pos.new(2, 1)))

          g.set(Tile.wall(pos: Pos.new(0, 2)))
          g.set(Tile.wall(pos: Pos.new(1, 2)))
          g.set(Tile.end(pos: Pos.new(2, 2)))
        end
      end

      subject { Maze.new(grid: grid, maze_start: Pos.new(0, 0), maze_end: Pos.new(3, 3)) }

      it "sets visibility" do
        subject.update_visibility_from(Pos.new(0, 0), workers: 0)

        [[0,0], [1,0], [0, 1], [1, 1], [2, 2]].each do |coord|
          expect(subject.at(Pos.new(*coord)).visible?).to be
        end

        [[2,0], [2, 1], [0,2], [1, 2]].each do |coord|
          expect(subject.at(Pos.new(*coord)).visible?).to_not be
        end
      end

      it "obeys the range constraint" do
        subject.update_visibility_from(Pos.new(0, 0), workers: 0, range: 1)

        [[0,0], [1,0], [0, 1], [1, 1]].each do |coord|
          expect(subject.at(Pos.new(*coord)).visible?).to be
        end

        [[2,0], [2, 1], [0,2], [1, 2], [2, 2]].each do |coord|
          expect(subject.at(Pos.new(*coord)).visible?).to_not be
        end
      end
    end
  end
end
