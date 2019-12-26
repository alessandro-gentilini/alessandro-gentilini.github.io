#include <iostream>
#include <utility>
#include <type_traits>
#include <vector>
#include <istream>
#include <ostream>
#include <iterator>
#include <sstream>
#include <string>
#include <fstream>

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

// https://stackoverflow.com/a/5148913
struct digits_only: std::ctype<char> {
    digits_only(): std::ctype<char>(get_table()) {}

    static std::ctype_base::mask const* get_table() {
        static std::vector<std::ctype_base::mask> 
            rc(std::ctype<char>::table_size,std::ctype_base::space);

        //std::fill(&rc['0'], &rc['9'], std::ctype_base::digit);
        std::fill(&rc['a'], &rc['z'], std::ctype_base::lower);
        std::fill(&rc['A'], &rc['Z'], std::ctype_base::upper);
        return &rc[0];
    }
};

// int main(int argc, char const *argv[])
// {
//     for (int i = 0; i < std::extent<decltype(T)>::value; i++)
//     {
//         auto r = f(i, std::extent<decltype(T)>::value, 0, std::extent<decltype(P)>::value);
//         if (r.second != 0)
//         {
//             std::cout << "loc=" << r.first - r.second << " len=" << r.second << "\n";
//         }
//     }
//     return 0;
// }

int main() {
    std::ifstream bible("pg10.txt");
    bible.imbue(std::locale(std::locale(), new digits_only));

    std::copy(std::istream_iterator<std::string>(bible),
              std::istream_iterator<std::string>(),
              std::ostream_iterator<std::string>(std::cout, " "));

    return 0;
}
