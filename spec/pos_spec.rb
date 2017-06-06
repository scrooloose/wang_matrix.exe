module WangMatrix

  RSpec.describe Pos do
    describe "#==" do
      it "is true if the coordinates are the same" do
        expect(Pos.new(1,1) == Pos.new(1,1)).to be
      end

      it "is false if the coordinates are different" do
        expect(Pos.new(1,1) == Pos.new(2,1)).to_not be
      end
    end

    describe "#up, #down, #left, #right" do
      subject { Pos.new(5,5) }

      it "up returns the position above" do
        expect(subject.up.to_a).to eq [5,4]
      end

      it "down returns the position below" do
        expect(subject.down.to_a).to eq [5,6]
      end

      it "left returns the position left" do
        expect(subject.left.to_a).to eq [4,5]
      end

      it "right returns the position right" do
        expect(subject.right.to_a).to eq [6,5]
      end
    end

    describe "#points_between" do
      it "returns an array positions" do
        expect(
          Pos.new(1, 1).points_between(Pos.new(4, 4))
        ).to eq [
          Pos.new(2, 2), Pos.new(3, 3)
        ]
      end

      it "returns an empty array for adjacent positions" do
        expect(
          Pos.new(1, 1).points_between(Pos.new(2, 2))
        ).to eq []
      end
    end
  end
end
