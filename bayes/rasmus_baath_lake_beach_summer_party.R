png()
temp<-c(19,23,20,17,23)
mu <- seq(8,30,by=.5)
sigma <- seq(.1,10,by=.3)
pars <- expand.grid(mu=mu, sigma=sigma)
pars$mu_prior <- dnorm(pars$mu,mean=18,sd=5)
#pars$mu_prior <- dunif(pars$mu,min=-30,max=50)
pars$sigma_prior <- dunif(pars$sigma,min=0,max=10)
pars$prior <- pars$mu_prior * pars$sigma_prior
for (i in 1:nrow(pars)) {
  likelihoods <- dnorm(temp,pars$mu[i],pars$sigma[i])
  pars$likelihood[i] <- prod(likelihoods)
}
pars$unnormalized_posterior <- pars$likelihood*pars$prior
pars$posterior <- pars$unnormalized_posterior/sum(pars$unnormalized_posterior)

library(lattice)
plot(levelplot(posterior~mu*sigma,data=pars))

sample_indices <- sample(1:nrow(pars), size=1e4, replace = TRUE, prob=pars$posterior)
pars_sample <- pars[sample_indices,c('mu','sigma')]
hist(pars_sample$mu,breaks = 30)
print(quantile(pars_sample$mu,c(0.05,0.95)))

predicted_temp <- rnorm(1e4,mean=pars_sample$mu,sd=pars_sample$sigma)
hist(predicted_temp,breaks=30)

print(sum(predicted_temp>=18)/length(predicted_temp))
