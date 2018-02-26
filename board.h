#include "env.h"

const int NUM_ANTS = 1;
const int DIM = 10;

class Board {

public:
    Board();
    ~Board();
    Obs *update(Action *a);

private:
    Tile board[DIM][DIM];

    Ant  ants        [NUM_ANTS];
    Obs  observations[NUM_ANTS];
};
