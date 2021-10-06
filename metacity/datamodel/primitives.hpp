#include <vector>
#include <map>

using namespace std;


template <class V, class F>
class Primitive
{
public:
    Primitive();
    virtual void transform() = 0;
    virtual map<string, string> serialize() const = 0;

protected:
    void append_vertex(const F *);
    vector<V> vertices;
};

template <class V, class F>
class MultiPoint : public Primitive<V, F>
{
public:
    MultiPoint();
    void add_points(const vector<F> ivertices);

protected:
};

template <class V, class F>
class MultiLine : public Primitive<V, F>
{
public:
    MultiLine();
    void add_line(const vector<F> ivertices);

protected:
};

template <class V, class F>
class MultiPolygon : public Primitive<V, F>
{
public:
    MultiPolygon();
    void add_polygon(const vector<vector<F>> ivertices);

protected:
    vector<vector<vector<V>>> polygons;
};
