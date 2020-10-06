#include <vector>
#include <iostream>
#include <cmath>
#include <sstream>

std::vector<double> sequence(double from, double to, double by)
{
    std::vector<double> v;
    if(from>to) return v;

    v.push_back(from);
    while(v.back()<to) v.push_back(v.back()+by);
    return v;
}

// https://mathworld.wolfram.com/GaussianFunction.html
double dnorm(double x, double mu, double sigma)
{
    return 1/(sigma*sqrt(2*M_PI))*exp(-pow(x-mu,2)/(2*pow(sigma,2)));
}

std::string head(const std::vector<double>& v)
{
    std::ostringstream oss;
    for(size_t i = 0; i < std::min(size_t(5),v.size()); i++){
        oss << v[i] << " ";
    }
    return oss.str();
}

double dunif(double x, double min, double max)
{
    if(x<min || x> max) return 0;
    return 1/(max-min);
}

double product(const std::vector<double>& v)
{
    double r = 1;
    for ( size_t i = 0; i < v.size(); i++){
        r *= v[i];
    }
    return r;
}

int main(int argc, char const *argv[])
{
    std::vector<double> temp={19,23,20,17,23};

    std::vector<double> mu_seq = sequence(8,30,.5);
    //std::cout << "mu: " << head(mu_seq) << "\n";
    
    std::vector<double> sigma_seq = sequence(.1,10,.3);
    //std::cout << "sigma: " << head(sigma_seq) << "\n";

    std::vector<double> mu;
    std::vector<double> sigma;
    std::vector<double> mu_prior;
    std::vector<double> sigma_prior;
    std::vector<double> prior;
    std::vector<double> likelihood;
    std::vector<double> unnormalized_posterior;
    double denominator = 0;

    for(size_t i = 0; i < sigma_seq.size(); i++){
        for(size_t j=0; j < mu_seq.size(); j++){
            mu.push_back(mu_seq[j]);
            sigma.push_back(sigma_seq[i]);
            mu_prior.push_back(dnorm(mu.back(),18,5));
            sigma_prior.push_back(dunif(sigma.back(),0,10));
            prior.push_back(mu_prior.back()*sigma_prior.back());
            std::vector<double> likelihoods;
            for(size_t k =0; k <temp.size(); k++){
                likelihoods.push_back(dnorm(temp[k],mu.back(),sigma.back()));
            }
            likelihood.push_back(product(likelihoods));
            unnormalized_posterior.push_back(prior.back()*likelihood.back());
            denominator += unnormalized_posterior.back();
        }
    }

    std::vector<double> posterior;
    for(size_t i = 0; i < unnormalized_posterior.size(); i++){
        posterior.push_back(unnormalized_posterior[i]/denominator);
    }

    std::cout << "mu,sigma,posterior\n";
    for(size_t i = 0; i < posterior.size(); i++)
    {
        std::cout << mu[i] << "," << sigma[i] << "," << posterior[i] << "\n";
    }
    
    
    return 0;
}
