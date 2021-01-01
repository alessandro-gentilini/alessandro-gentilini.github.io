#include <iostream>
#include <math.h>
#include <vector>


double cardinal_sin(double x)
{
    //return exp(-x*x);
    //return x*x-50;
    //return 1-exp(-x);
    //return sin(x);
    if(x==0) return 1;
    return sin(x)/x;
}

std::vector<double> linspace(double m, double M, size_t N)
{
    std::vector<double> result;
    if(m>M || N==0) return result;

    double delta = (M-m)/N;
    double x = m;
    while(x<=M){
        result.push_back(x);
        x += delta;
    }
    
    return result;
}

std::vector<double> linear_scale(double a, double b, double A, double B)
{
    double m = (A-B)/(a-b);
    double q = B-m*b;
    std::vector<double> result;
    result.push_back(m);
    result.push_back(q);
    return result;
}

int main(int,char**)
{
    const double X_min = 0;
    const double X_max = 80;
    const double Y_min = 0;
    const double Y_max = 30;

    char S[size_t(X_max+1)][size_t(Y_max+1)];
    for(size_t i = 0; i < X_max+1; i++){
        for(size_t j = 0; j < Y_max+1; j++){
            S[i][j]=' ';
        }
    }

    double x_min = -4*M_PI;
    double x_max = 4*M_PI;
    auto x = linspace(x_min,x_max,100);
    std::vector<double> y;
    double y_min = __DBL_MAX__;
    double y_max = -y_min;
    for(size_t i = 0; i < x.size(); i++){
        y.push_back(cardinal_sin(x[i]));
        if(y.back()<y_min) y_min = y.back();
        if(y.back()>y_max) y_max = y.back();
    }

    auto mq_x = linear_scale(x_min,x_max,X_min,X_max);
    auto mq_y = linear_scale(y_min,y_max,Y_min,Y_max);

    for(size_t i = 0; i < x.size(); i++){
        double X = round(mq_x[0]*x[i]+mq_x[1]);
        double Y = round(mq_y[0]*y[i]+mq_y[1]);
        for(size_t j=0; j<Y_max+1; j++){
            if( j == Y ){
                S[size_t(X)][j] = '*';
            } else {
                if(j==round(mq_y[1])){
                    S[size_t(X)][j] = '|';
                } else {
                    S[size_t(X)][j] = ' ';
                }
            }
        }
    }

    for(size_t j=0; j<Y_max+1; j++){
        if(S[size_t(round(mq_x[1]))][j]!='*'){
            S[size_t(round(mq_x[1]))][j]='-';
        }
    }    

    for(int i = Y_max; i >= 0; i--){
        for(size_t j = 0; j < X_max+1; j++){
            std::cout << S[j][i];
        }
        std::cout << '\n';
    }

    
    return 0;
}