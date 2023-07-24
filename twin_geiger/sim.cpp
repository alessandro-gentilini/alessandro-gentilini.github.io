//jack@giangrandi.ch
#include <random>
#include <iostream>

const size_t N = 1000;
const int M = 1000;
double p_choice = .5;
double p_lost = .5;
double dead_time_0 = 1000;
double dead_time_1 = 10;

int select()
{
    return rand() / double(RAND_MAX) < p_choice ? 0 : 1;
}

bool lost()
{
    return rand() / double(RAND_MAX) < p_lost ? 0 : 1;
}

int main()
{
    srand(time(NULL));
    double e[N];
    e[0] = 0;
    for(size_t i = 1; i < N; i++) {
        //double next = M*rand()/double(RAND_MAX);
        double next = rand()/double(RAND_MAX);
        double next2 = M*next;
        std::cout << next << "\t" << next2 << "\n";
        e[i] = e[i-1] + next2;
    }
    bool busy_0 = false;
    bool busy_1 = false;
    size_t cnt_0 = 0;
    size_t cnt_1 = 0;
    double t_busy_0 = 0;
    double t_busy_1 = 0;
    for(size_t i = 0; i < N; i++) {
        if(busy_0 && t_busy_0+dead_time_0<e[i]){
            busy_0 = false;
        }
        if(busy_1 && t_busy_1+dead_time_1<e[i]){
            busy_1 = false;
        }        
        if(select()==0) {
            if(!busy_0){
                busy_0 = true;
                cnt_0++;
                t_busy_0 = e[i];
            } else if(!lost()&&!busy_1){
                busy_1 = true;
                cnt_1++;
                t_busy_1 = e[i];                
            }
        } else {
            if(!busy_1){
                busy_1 = true;
                cnt_1++;
                t_busy_1 = e[i];
            } else if(!lost()&&!busy_0){
                busy_0 = true;
                cnt_0++;
                t_busy_0 = e[i];                
            }           
        }
        std::cout << i << "\t" << e[i] << "\t" << cnt_0 << "\t" << cnt_1 << "\n";
    }

    std::cout << cnt_0 << "\t" << cnt_1 << "\t" << cnt_0+cnt_1<< "\n";

    return 0;
}