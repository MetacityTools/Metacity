#include <vector>
#include "types.hpp"
#include "timepoints.hpp"

using namespace std;


class Interval {
public:
    Interval(uint32_t time_start, uint32_t length);
    void insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid);
    bool can_contain(shared_ptr<MultiTimePoint> timepoints);

protected:
    //TODO


    vector<vector<...>> buffers;
};