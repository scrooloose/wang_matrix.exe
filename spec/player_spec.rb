module WangMatrix
  RSpec.describe Player do
    describe "#move_up, #move_down, #move_left, #move_right" do
      subject { Player.new(pos: Pos.new(5,5), maze: maze) }

      context "move is legal" do
        let(:maze) do
          instance_double("Maze", "traversable?" => true, update_visibility_from: true)
        end

        it "moves left" do
          expect(subject.move_left.pos.to_a).to eq [4,5]
        end

        it "moves right" do
          expect(subject.move_right.pos.to_a).to eq [6,5]
        end

        it "moves up" do
          expect(subject.move_up.pos.to_a).to eq [5,4]
        end

        it "moves down" do
          expect(subject.move_down.pos.to_a).to eq [5,6]
        end
      end

      context "move is illegal" do
        let(:maze) { instance_double("Maze", "traversable?" => false) }

        it "doesn't move" do
          expect { subject.move_left }.to_not change {subject.pos}
        end
      end
    end
  end
end
