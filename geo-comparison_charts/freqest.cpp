#include <iostream>
#include <sstream>
#include <random>

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
void SutherlandHodgman(point2D *subjectPolygon, int &subjectPolygonSize, point2D *clipPolygon, int &clipPolygonSize, point2D (&newPolygon)[N], int &newPolygonSize)
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
    for (size_t i = 0; i < p.size(); i++){
        oss << "[" << p[i].x << "," << p[i].y << "]";
        if(i!=p.size()-1){
            oss << ",";
        }
    }
    oss << "]";
    return oss.str();
}

int main(int argc, char **argv)
{
    // subject polygon
    point2D subjectPolygon[] = {
        {50, 150}, {200, 50}, {350, 150}, {350, 300}, {250, 300}, {200, 250}, {150, 350}, {100, 250}, {100, 200}};
    int subjectPolygonSize = sizeof(subjectPolygon) / sizeof(subjectPolygon[0]);

    // clipping polygon
    point2D clipPolygon[] = {{100, 100}, {300, 100}, {300, 300}, {100, 300}};
    int clipPolygonSize = sizeof(clipPolygon) / sizeof(clipPolygon[0]);

    // define the new clipped polygon (empty)
    int newPolygonSize = 0;
    point2D newPolygon[N] = {0};

    // apply clipping
    SutherlandHodgman(subjectPolygon, subjectPolygonSize, clipPolygon, clipPolygonSize, newPolygon, newPolygonSize);

    // print clipped polygon points
    //cout << "Clipped polygon points:" << endl;
    for (int i = 0; i < newPolygonSize; i++)
    {
        //cout << "(" << newPolygon[i].x << ", " << newPolygon[i].y << ")" << endl;
    }

    std::random_device rd{};
    std::mt19937 gen{rd()};

    // values near the mean are the most likely
    // standard deviation affects the dispersion of generated values from the mean
    std::normal_distribution<> w_d{5, 2};
    std::normal_distribution<> h_d{5, 2};

    std::normal_distribution<> a_d{0, 2};

    const float limit_x = 700;
    const float limit_y = 700;
    const float radius = 300;

    const float W = limit_x;
    const float H = (limit_y - 2 * radius) / 2;

    point2D circle_center = {limit_x / 2, limit_y / 2};

    std::vector<point2D> approx_circle;
    size_t N = 50;
    for (size_t i = 0; i < N; i++)
    {
        float theta = i / N * 2 * M_PI;
        float x = circle_center.x + radius * cos(theta);
        float y = circle_center.y + radius * sin(theta);
        approx_circle.push_back({x, y});
    }

    std::cout << "[\n";
    std::cout << polygon_to_JSON(std::vector<point2D>(clipPolygon, clipPolygon + clipPolygonSize));
    std::cout << ",\n";
    std::cout << polygon_to_JSON(rotate_r(std::vector<point2D>(clipPolygon, clipPolygon + clipPolygonSize), M_PI_4));
    std::cout << "\n";
    std::cout << "]\n";

    return 0;
}