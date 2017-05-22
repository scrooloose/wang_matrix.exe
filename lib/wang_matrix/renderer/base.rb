module WangMatrix
  module Renderer
    class Base
      def perform(**args)
        raise NotImplementedError
      end

      def present_solution(**args)
        raise NotImplementedError
      end

      def reset_screen(**args)
        raise NotImplementedError
      end
    end
  end
end
