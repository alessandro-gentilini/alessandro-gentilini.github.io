#include <iostream>
#include <utility>
#include <type_traits>

int T[] = {3, 1, 4, 3, 1};
int P[] = {3, 1, 4, 1, 5};

std::pair<int, int> f(int t, int Tsz, int p, int Psz)
{
    if (T[t] == P[p] && t + 1 <= Tsz && p + 1 <= Psz)
    {
        f(t + 1, Tsz, p + 1, Psz);
    }
    else
    {
        return std::make_pair(t, p);
    }
}

int main(int argc, char const *argv[])
{
    for (int i = 0; i < std::extent<decltype(T)>::value; i++)
    {
        auto r = f(i, std::extent<decltype(T)>::value, 0, std::extent<decltype(P)>::value);
        if (r.second != 0)
        {
            std::cout << "loc=" << r.first - r.second << " len=" << r.second << "\n";
        }
    }
    return 0;
}
