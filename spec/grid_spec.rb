module WangMatrix
  RSpec.describe Grid do
    let(:tile) { Tile.wall(pos: Pos.new(1,1)) }
    subject do
      Grid.new(width: 5, height: 5).tap { |g| g.set(tile) }
    end

    describe "#at" do
      it "finds the atxy" do
        expect(subject.at(Pos.new(1, 1))).to eq(tile)
      end
    end

    describe "#atxy" do
      it "finds the object" do
        expect(subject.atxy(1, 1)).to eq(tile)
      end
    end

    describe "#set" do
      it "adds the object" do
        expect(subject.atxy(1, 1)).to eq(tile)
      end
    end

    describe "#find" do
      it "returns the first matching tile found" do
        expect(subject.find("#")).to eq tile
      end
    end

    describe "#clone" do
      it "returns a copy" do
        expect {
          clone = subject.clone
          clone.set(Tile.space(pos: Pos.new(2,2)))
        }.not_to change { subject.atxy(2,2) }
      end
    end

    describe "#to_s" do
      subject do
        Grid.new(width: 2, height: 2).tap do |g|
          g.set(Tile.wall(pos: Pos.new(1,1), visible: true))
          g.set(Tile.wall(pos: Pos.new(0,1), visible: false))
        end
      end

      context "force_visible: true" do
        it "renders invisible tiles" do
          expect(subject.to_s(force_visible: true)).to eq("  \n##")
        end
      end

      context "without force_visible" do
        it "only renders visible tiles" do
          expect(subject.to_s).to eq("  \n #")
        end
      end
    end

    describe "#each" do
      subject { Grid.new(width: 2, height: 2) }

      it "yields each tile" do
        positions = []
        subject.each { |t| positions << t.pos.to_a }
        expect(positions).to eq([[0,0], [1,0], [0,1], [1,1]])
      end
    end
  end
end
