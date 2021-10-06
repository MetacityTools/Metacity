#include "primitives.hpp"
#include <stdexcept>



template <class V, class F>
void Primitive<V, F>::append_vertex(const F *vertex)
{
    vertices.emplace_back(V(vertex));
}

template <class V, class F>
void MultiPoint<V, F>::add_points(const vector<F> iv)
{
    if (iv.size() % V::size())
        throw runtime_error("Unexpected number of elements in input array");

    this->vertices.insert(this->vertices.end(), iv.begin(), iv.end());
}


template <class V, class F>
void MultiLine<V, F>::add_line(const vector<F> iv)
{
    if ((iv.size() % V::size()) || (iv.size() < V::size() * 2))
        throw runtime_error("Unexpected number of elements in input array");

    for (const float e : iv)
    {
        this->vertices.insert(this->vertices.end(), iv.begin(), iv.end());
    }
}


template <class V, class F>
void MultiPolygon<V, F>::add_polygon(const vector<vector<F>> iv)
{
}