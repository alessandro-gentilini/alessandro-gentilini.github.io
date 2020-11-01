# Estimation of the Epicentral Coordinates of a Seismic Event
# TARANTOLA, Albert. Inverse problem theory and methods for model parameter estimation. Society for Industrial and Applied Mathematics, 2005.
png()
library(rstan)

data <- data.frame(x=c(3,3,4,4,5,5),
y=c(15,16,15,16,15,16),
t=c(3.12,3.26,2.98,3.12,2.84,2.98),
t0=c(0,0,0,0,0,0),
v=c(5,5,5,5,5,5)
)
str(data)


model1 <- '
data{
    vector[6] t;
    real v[6];
    real y[6];
    real x[6];
    real t0[6];
}
parameters{
    real<lower=-100,upper=100> x0;
    real<lower=-100,upper=100> y0;
}
model{
    vector[6] mu;
    y0 ~ uniform( -100 , 100 );
    x0 ~ uniform( -100 , 100 );
    for ( i in 1:6 ) {
        mu[i] = t0[i] + sqrt((x[i] - x0)^2 + (y[i] - y0)^2)/v[i];
    }
    t ~ normal( mu , .1 );
}'

sm <- stan_model(model_code = model1)

fit1 <- sampling(sm, data = data, iter = 4000, chains=2, refresh = 0)
print(fit1)
pairs(fit1)
plot(fit1)
plot(fit1, show_density = TRUE, ci_level = 0.5, fill_color = "purple")

library(ggplot2)
library(bayesplot)

p2 <- mcmc_scatter(fit1, pars = c("x0", "y0"), size = 3.5, alpha = 0.25)
p2 + stat_density_2d(color = "black", size = .5) + coord_equal(xlim=c(0,20),ylim=c(0,20))
