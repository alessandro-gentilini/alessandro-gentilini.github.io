pop <- 5.806e6
brown <- ceiling(.417*pop)
green <- ceiling(.424*pop)
other <- pop-(brown+green)

sample_size <- 7422
brown_in_sample <- ceiling(.384*sample_size)
green_in_sample <- ceiling(.444*sample_size)
other_in_sample <- sample_size-(brown_in_sample+green_in_sample)

stat <- function(pop1, pop2, sample_size) {
  abs( pop1 - pop2 ) / sample_size
}

# brown=1, green=2, other=0
universe <- c( rep(1,brown),
               rep(2,green),
               rep(0,other))

n.sims <- 10000

replicate(n.sims, {
  sampling <- sample(universe, sample_size, rep=FALSE) 
  n.browns <- length( sampling[sampling==1] )
  n.greens <- length( sampling[sampling==2] )
  stat(n.browns, n.greens, sample_size)
}) -> results

observed.effect <- stat(brown_in_sample, green_in_sample, sample_size)

compute.p.value <- function(results, observed.effect, precision=3) {
  # n = #experiences
  n <- length(results)
  # r = #replications at least as extreme as observed effect
  r <- sum(abs(results) >= observed.effect)  
  # compute Monte Carlo p-value with correction (Davison & Hinkley, 1997)
  list(mc.p.value=round((r+1)/(n+1), precision), r=r, n=n)
}

present_results <- function(results, observed.effect, label="", breaks=50, precision=3) {
  lst <- compute.p.value(results, observed.effect, precision=precision)
  
  hist(results, breaks=breaks, prob=T, main=label, col = "dodgerblue",
       #sub=paste0("MC p-value for H0: ", lst$mc.p.value), 
       xlim=c(0,1.2*max(c(results,observed.effect))),
       #xlab=paste("found", lst$r, "as extreme effects for", lst$n, "replications"))
       xlab='Gruppo A meno Gruppo 0, espresso come frazione (1=100%)')
  abline(v=observed.effect, lty=2, lwd=2, col="red")
}

present_results(results, observed.effect)

model1="data { 
  int<lower=2> m;     // at least two groups
  int<lower=1> n[m]; 
  int<lower=0> k[m]; 
} 

parameters {
  real<lower=0,upper=1> theta[m];
} 

model {
  theta ~ beta(1, 1);

  k ~ binomial(n, theta);
}

generated quantities {
  real delta[m,m];
  
  for ( i in 1:m ) {
     for ( j in 1:m ) {
        if (i==j)
           delta[i,j] = normal_lpdf(0|0,1); // dummy values
         else 
           delta[i,j] = theta[i] - theta[j];
     }
  }
}" 

library(rstan)
library(rethinking)
#library(latex2exp)

n <- c(pop, sample_size )       # runs
k <- c(brown, brown_in_sample ) # successes
m <- length(n)

sm <- stan_model(model_code = model1)

# model1 is a string containing the Stan model above
fit1 <- sampling(sm,
                 data    = list(n=n, k=k, m=m),
                 iter    = 10000,
                 chains  = 2,
                 refresh = 0
)

precis(fit1, depth=3, prob=0.99)

samples <- rstan::extract(fit1)

samples_theta <- samples$theta
samples_delta <- samples$delta

credible_interval <- PI(samples_delta[,1,2], prob=0.99)
h <- hist(samples_delta[,1,2], breaks=40, prob=T, yaxt='n',
          col=rgb(0,0,1,0.15), border=rgb(1,1,1,0.6), main="",
          #xlab=TeX(paste0('$\\theta_',1,'-\\theta_',2,'$'))
          xlab='Gruppo A meno Gruppo 0, espresso come frazione (1=100%)'
          , ylab="")

y.seg <- max(h$density) / 15
segments(credible_interval[1], y.seg, credible_interval[2], y.seg, 
        lwd=5, col="dodgerblue")
text(credible_interval[1], y.seg*2.5, round(credible_interval[1],3), 
    col="dodgerblue")
text(credible_interval[2], y.seg*2.5, round(credible_interval[2],3), 
    col="dodgerblue")