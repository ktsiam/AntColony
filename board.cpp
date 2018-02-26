#include "board.h"
#include "env.h"

#include <vector>


Board::Board() {
    // initialize Tiles
    for (int i = 0; i < DIM; i++) {
        for (int j = 0; j < DIM; ) {
            board[i][j] = Tile(i,j);
        }
    }
    for (int i = 0; i < NUM_ANTS; i++) {
        ants[i] = Ant(i);
    }

}
