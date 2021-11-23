#include <vector>
#include "types.hpp"
#include "timepoints.hpp"

using namespace std;

struct Movement {
    tvec3 from;
    tvec3 to;
    int32_t oid;
};

class Interval {
public:
    Interval(uint32_t interval_start_time_, uint32_t interval_length);
    void insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid);
    bool can_contain(shared_ptr<MultiTimePoint> timepoints);

protected:
    //TODO
    uint32_t start_time;
    uint32_t length;
    vector<vector<Movement>> buffers;
};