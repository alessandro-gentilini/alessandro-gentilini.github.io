#include <iostream>
#include <sstream>
#include <random>
#include <algorithm>

// https://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping#C.2B.2B
using namespace std;

struct point2D
{
    float x, y;
};

const int N = 99; // clipped (new) polygon size

// check if a point is on the LEFT side of an edge
bool inside(point2D p, point2D p1, point2D p2)
{
    return (p2.y - p1.y) * p.x + (p1.x - p2.x) * p.y + (p2.x * p1.y - p1.x * p2.y) < 0;
}

// calculate intersection point
point2D intersection(point2D cp1, point2D cp2, point2D s, point2D e)
{
    point2D dc = {cp1.x - cp2.x, cp1.y - cp2.y};
    point2D dp = {s.x - e.x, s.y - e.y};

    float n1 = cp1.x * cp2.y - cp1.y * cp2.x;
    float n2 = s.x * e.y - s.y * e.x;
    float n3 = 1.0 / (dc.x * dp.y - dc.y * dp.x);

    return {(n1 * dp.x - n2 * dc.x) * n3, (n1 * dp.y - n2 * dc.y) * n3};
}

// Sutherland-Hodgman clipping
void SutherlandHodgman(const point2D *subjectPolygon, const size_t &subjectPolygonSize, const point2D *clipPolygon, const size_t &clipPolygonSize, point2D (&newPolygon)[N], int &newPolygonSize)
{
    point2D cp1, cp2, s, e, inputPolygon[N];

    // copy subject polygon to new polygon and set its size
    for (int i = 0; i < subjectPolygonSize; i++)
        newPolygon[i] = subjectPolygon[i];

    newPolygonSize = subjectPolygonSize;

    for (int j = 0; j < clipPolygonSize; j++)
    {
        // copy new polygon to input polygon & set counter to 0
        for (int k = 0; k < newPolygonSize; k++)
        {
            inputPolygon[k] = newPolygon[k];
        }
        int counter = 0;

        // get clipping polygon edge
        cp1 = clipPolygon[j];
        cp2 = clipPolygon[(j + 1) % clipPolygonSize];

        for (int i = 0; i < newPolygonSize; i++)
        {
            // get subject polygon edge
            s = inputPolygon[i];
            e = inputPolygon[(i + 1) % newPolygonSize];

            // Case 1: Both vertices are inside:
            // Only the second vertex is added to the output list
            if (inside(s, cp1, cp2) && inside(e, cp1, cp2))
                newPolygon[counter++] = e;

            // Case 2: First vertex is outside while second one is inside:
            // Both the point of intersection of the edge with the clip boundary
            // and the second vertex are added to the output list
            else if (!inside(s, cp1, cp2) && inside(e, cp1, cp2))
            {
                newPolygon[counter++] = intersection(cp1, cp2, s, e);
                newPolygon[counter++] = e;
            }

            // Case 3: First vertex is inside while second one is outside:
            // Only the point of intersection of the edge with the clip boundary
            // is added to the output list
            else if (inside(s, cp1, cp2) && !inside(e, cp1, cp2))
                newPolygon[counter++] = intersection(cp1, cp2, s, e);

            // Case 4: Both vertices are outside
            else if (!inside(s, cp1, cp2) && !inside(e, cp1, cp2))
            {
                // No vertices are added to the output list
            }
        }
        // set new polygon size
        newPolygonSize = counter;
    }
}

std::vector<point2D> translate(const std::vector<point2D> &rect, const point2D &t)
{
    point2D a = {rect[0].x + t.x, rect[0].y + t.y};
    point2D b = {rect[1].x + t.x, rect[1].y + t.y};
    point2D c = {rect[2].x + t.x, rect[2].y + t.y};
    point2D d = {rect[3].x + t.x, rect[3].y + t.y};
    return {a, b, c, d};
}

point2D rotate(const point2D &p, const float &theta)
{
    return {p.x * cos(theta) - p.y * sin(theta), p.x * sin(theta) + p.y * cos(theta)};
}

std::vector<point2D> rotate_r(const std::vector<point2D> &rect, const float &theta)
{
    auto a = rotate(rect[0], theta);
    auto b = rotate(rect[1], theta);
    auto c = rotate(rect[2], theta);
    auto d = rotate(rect[3], theta);
    return {a, b, c, d};
}

std::vector<point2D> rect(const float &b, const float &h)
{
    return {{0, 0}, {b, 0}, {b, h}, {0, h}};
}

std::string polygon_to_JSON(const std::vector<point2D> &p)
{
    std::ostringstream oss;
    oss << "[";
    for (size_t i = 0; i < p.size(); i++)
    {
        oss << "[" << p[i].x << "," << p[i].y << "]";
        if (i != p.size() - 1)
        {
            oss << ",";
        }
    }
    oss << "]";
    return oss.str();
}

float distance(const point2D &p1, const point2D &p2)
{
    return hypot(p1.x - p2.x, p1.y - p2.y);
}

bool is_outside(const std::vector<point2D> &rect, const point2D &circle_center, float circle_radius)
{
    return distance(rect[0], circle_center) > circle_radius &&
           distance(rect[1], circle_center) > circle_radius &&
           distance(rect[2], circle_center) > circle_radius &&
           distance(rect[3], circle_center) > circle_radius;
}

float determinant(const point2D &p1, const point2D &p2)
{
    float x1 = p1.x;
    float y1 = p1.y;
    float x2 = p2.x;
    float y2 = p2.y;
    return x1 * y2 - x2 * y1;
}

// http://mathworld.wolfram.com/PolygonArea.html
float polygon_area(const std::vector<point2D> &p)
{
    float A = 0;
    size_t sz = p.size();
    for (size_t i = 0; i < sz; i++)
    {
        A += determinant(p[i], p[(i + 1) % sz]);
    }
    return std::abs(A / 2);
}

bool are_overlapped(const std::vector<point2D> &r1, const std::vector<point2D> &r2)
{
    // define the new clipped polygon (empty)
    int newPolygonSize_a = 0;
    point2D newPolygon_a[N] = {0};

    int newPolygonSize_b = 0;
    point2D newPolygon_b[N] = {0};

    // apply clipping
    SutherlandHodgman(&r1[0], r1.size(), &r2[0], r2.size(), newPolygon_a, newPolygonSize_a);
    SutherlandHodgman(&r2[0], r2.size(), &r1[0], r1.size(), newPolygon_b, newPolygonSize_b);

    return newPolygonSize_a > 0 || newPolygonSize_b > 0;
}

struct {
    bool operator()(const std::vector<point2D> &a, const std::vector<point2D> &b) const 
    { 
        std::vector aa{a[0].x,a[0].y};
        std::vector bb{b[0].x,b[0].y};
        return std::lexicographical_compare(aa.begin(),aa.end(),bb.begin(),bb.end());
    }
} customLess;

int main(int argc, char **argv)
{
    std::default_random_engine dre; 

    // values near the mean are the most likely
    // standard deviation affects the dispersion of generated values from the mean
    std::normal_distribution<float> w_d{15, 2};
    std::normal_distribution<float> h_d{10, 2};

    std::normal_distribution<float> a_d{0, .1};


    const float limit_x = 700;
    const float limit_y = 700;
    const float radius = 300;

    std::uniform_int_distribution<> ux_d(0,limit_x);
    std::uniform_int_distribution<> uy_d(0,limit_y);

    const float W = limit_x;
    const float H = (limit_y - 2 * radius) / 2;

    point2D circle_center = {limit_x / 2, limit_y / 2};

    std::vector<point2D> approx_circle;
    size_t NN = 50;
    for (size_t i = 0; i < NN; i++)
    {
        float theta = float(i) / NN * 2 * M_PI;
        float x = circle_center.x + radius * cos(theta);
        float y = circle_center.y + radius * sin(theta);
        approx_circle.push_back({x, y});
    }

    float approx_circle_area = polygon_area(approx_circle);

    std::vector<std::vector<point2D>> rr;
    float particle_area = 0;
    float w;
    float h;
    float frequency = 0;
    float target_frequency = 50;
    size_t idx = 0;
    std::vector<point2D> r;
    std::cerr << "idx,freq\n";    
    do
    {
        std::cerr << idx++ << "," << frequency << "\n";
        w = w_d(dre);
        h = h_d(dre);
        if (w <= 0 || h <= 0)
            continue;
        r = translate(rotate_r(rect(w, h), a_d(dre)), {float(ux_d(dre)), float(uy_d(dre))});
        if (is_outside(r, circle_center, radius))
            continue;
        bool overlap = false;
        for (size_t i = 0; i < rr.size() && !overlap; i++)
        {
            overlap = are_overlapped(r, rr[i]);
        }
        if (!overlap)
        {
            // define the new clipped polygon (empty)
            int clippedSize = 0;
            point2D clipped[N] = {0};

            // apply clipping
            SutherlandHodgman(&r[0], r.size(), &approx_circle[0], approx_circle.size(), clipped, clippedSize);
            if (clippedSize)
            {
                particle_area += polygon_area(std::vector<point2D>(clipped,clipped+clippedSize));
                rr.push_back(r);
                std::sort(rr.begin(),rr.end(),customLess);
            }
        }
        frequency = 100 * particle_area / approx_circle_area;
    } while (frequency < target_frequency);

    std::cout << "[\n";        
    for (size_t i = 0; i < rr.size(); i++){
        std::cout << polygon_to_JSON(rr[i]);
        if(i!=rr.size()-1){
            std::cout << ",\n";
        }

    }
    std::cout << "\n]\n";    

    return 0;
}