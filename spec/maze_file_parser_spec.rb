module WangMatrix
  RSpec.describe MazeFileParser do
    describe "#perform" do
      it "returns the maze as expected" do
        maze = described_class.new.perform(SpecHelpers.fixture_fpath("1.maze"))
        expect(maze.to_grid.to_s(force_visible: true)).to eq(
          "###\n" +
          "s.e\n" +
          "#*#\n" +
          " * \n" +
          "#*#\n" +
          "#.#\n" +
          "###"
        )
      end
    end
  end
end
