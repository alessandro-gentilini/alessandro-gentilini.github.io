#include <iostream>
#include <map>

int T[] = {3,1,4};
int P[] = {3,1,4,1,5};

std::pair<int,int> f(int t, int Tsz, int p, int Psz)
{
    if(T[t]==P[p] && t+1<=Tsz && p+1<=Psz){
        f(t+1,Tsz,p+1,Psz);
    } else {
        return std::make_pair(t,p);
    }
}

int main(int argc, char const *argv[])
{
    auto r = f(0,3,0,5);
    if(r.second!=0){
        std::cout << "loc=" << r.first-r.second << " len=" << r.second << "\n";
    }
    return 0;
}
