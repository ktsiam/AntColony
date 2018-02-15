#include <vector>

struct Ant;

struct Tile {
        std::vector<Ant*> ant_vec;
        float food;
        float trail;
};

struct Action {
        float forw;
        float rot;
};

struct Obs {
        float food [9];
        float trail[9];
};

struct Ant {

        void update(Obs &obs, Action a);
        Tile *tile;
        int food;
        double x, y;
        int id;
        
};
