// For build see http://userguide.icu-project.org/howtouseicu
// c++ -o pilit pilit.cpp `pkg-config --libs --cflags icu-uc icu-io`

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
#include <algorithm>

#include <unicode/utypes.h>
#include <unicode/unistr.h>
#include <unicode/translit.h>

std::string desaxUTF8(const std::string& str) {
    // UTF-8 std::string -> UTF-16 UnicodeString
    UnicodeString source = UnicodeString::fromUTF8(StringPiece(str));

    // Transliterate UTF-16 UnicodeString
    UErrorCode status = U_ZERO_ERROR;
    Transliterator *accentsConverter = Transliterator::createInstance(
        "NFD; [:M:] Remove; NFC", UTRANS_FORWARD, status);
    accentsConverter->transliterate(source);
    // TODO: handle errors with status

    // UTF-16 UnicodeString -> UTF-8 std::string
    std::string result;
    source.toUTF8String(result);

    return result;
}

int P[] = {3,1,4,1,5,9,2,6,5,3,5,8,9};

std::pair<int, int> f(int t, int Tsz, int p, int Psz, const std::vector<int>& sizes)
{
    if (sizes[t] == P[p] && t + 1 <= Tsz && p + 1 <= Psz)
    {
        f(t + 1, Tsz, p + 1, Psz, sizes);
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
        std::fill(&rc['a'], &rc['z']+1, std::ctype_base::lower);
        std::fill(&rc['A'], &rc['Z']+1, std::ctype_base::upper);
        return &rc[0];
    }
};

int main(int argc, char** argv) 
{
    if(argc<=1) std::cout << argv[0] << " text\n";
    std::ifstream bible(argv[1]);
    bible.imbue(std::locale(std::locale(), new digits_only));

    std::vector<std::string> words;
    std::copy(std::istream_iterator<std::string>(bible),
              std::istream_iterator<std::string>(),
              std::back_inserter(words));
              
    std::vector<int> sizes;
    std::transform(words.begin(), words.end(), std::back_inserter(sizes),
                   [](const std::string& s) -> std::size_t { return s.length(); });

    for(size_t i = 0; i < sizes.size(); i++){
        auto r = f(i,sizes.size(),0,std::extent<decltype(P)>::value,sizes);
         if (r.second != 0 && r.second>=5)
         {
             auto loc = r.first - r.second;
             auto len = r.second;
             std::cout << "loc=" << loc << " len=" << len << " ";
             for(size_t j = loc; j < loc+len; j++ ){
                 std::cout << words[j] << " ";
             }
             std::cout << "\n";
         }
    }

    return 0;
}
