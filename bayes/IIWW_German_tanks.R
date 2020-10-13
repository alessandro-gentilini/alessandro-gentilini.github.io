png()
n<-c(10, 256, 202, 97)
N <- seq(max(n),1e4,by=1)
pars <- expand.grid(N=N)
# The following prior knows about my data
# pars$N_prior <- dunif(pars$N,max(n),1e4)

# The following prior ignores my data
pars$N_prior <- dunif(pars$N,0,1e4)
pars$prior <- pars$N_prior
for (i in 1:nrow(pars)) {
  likelihoods <- dunif(n,0,pars$N[i])
  pars$likelihood[i] <- prod(likelihoods)
}
pars$unnormalized_posterior <- pars$likelihood*pars$prior
pars$posterior <- pars$unnormalized_posterior/sum(pars$unnormalized_posterior)

# library(lattice)
# plot(levelplot(posterior~mu*sigma,data=pars))

sample_indices <- sample(1:nrow(pars), size=1e4, replace = TRUE, prob=pars$posterior)
pars_sample <- pars[sample_indices,'N']
hist(pars_sample,breaks = 30)
print(mean(pars_sample))
print(sd(pars_sample))
print(quantile(pars_sample,c(0.025,0.975)))

# predicted_temp <- rnorm(1e4,mean=pars_sample$mu,sd=pars_sample$sigma)
# hist(predicted_temp,breaks=30)

# print(sum(predicted_temp>=18)/length(predicted_temp))
