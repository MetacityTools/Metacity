#include "glm/glm.hpp"
#include "json/pybind11_json.hpp"
#include <vector>

using tvec3 = glm::vec3;
using tvec2 = glm::vec2;
using tfloat = float;
using json = nlohmann::json;

using namespace std;

using Polygon = vector<vector<tvec3>>;
using Polygons = vector<vector<vector<tvec3>>>;