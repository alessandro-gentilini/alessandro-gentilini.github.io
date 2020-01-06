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



int main(int argc, char** argv) 
{
    int i = 0;
    while(std::cin){
        std::string w;
        std::cin >> w;
        std::cout << desaxUTF8(w) << (i++%20==0?"\n":" ");
    }

    return 0;
}
