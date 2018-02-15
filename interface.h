#include "board.h"

class Interface {
        
public:
        Interface();
        ~Interface();
        Obs *step(float *data);
        void reset();
        void render();

private:
        Board board;
};
