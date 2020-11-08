# Esempio di stima bayesiana del numero di elementi difettosi presenti in
# una popolazione di dimensione nota basato sul numero di elementi difettosi 
# trovati in un campione casuale estratto dalla popolazione.
png('proportion_from_a_finite_universe-%d.png')

# con likelihood esatta, che presuppone che si conosca il fatto che la likelihood
# è una ipergeometrica
dimensione_della_popolazione <- 100
dimensione_del_campione <- 10
difettosi_nel_campione <-c(1)
difettosi_nella_popolazione <- seq(0,dimensione_della_popolazione,by=1)
pars <- expand.grid(difettosi_nella_popolazione=difettosi_nella_popolazione)

pars$difettosi_nella_popolazione_prior <- dunif(pars$difettosi_nella_popolazione,0,dimensione_della_popolazione)
#pars$difettosi_nella_popolazione_prior <- dnorm(pars$difettosi_nella_popolazione,10,1)
pars$prior <- pars$difettosi_nella_popolazione_prior
for (i in 1:nrow(pars)) {
  likelihoods <- dhyper(difettosi_nel_campione,pars$difettosi_nella_popolazione[i],dimensione_della_popolazione-pars$difettosi_nella_popolazione[i],dimensione_del_campione)
  pars$likelihood[i] <- prod(likelihoods)
}
pars$unnormalized_posterior <- pars$likelihood*pars$prior
pars$posterior <- pars$unnormalized_posterior/sum(pars$unnormalized_posterior)

sample_indices <- sample(1:nrow(pars), size=1e4, replace = TRUE, prob=pars$posterior)
pars_sample <- pars[sample_indices,'difettosi_nella_popolazione']
print(head(pars_sample))

print(mean(pars_sample))
print(sd(pars_sample))
q = quantile(pars_sample,c(0.025,0.975))
print(q)

hist(pars_sample,breaks=difettosi_nella_popolazione-.5,freq=TRUE,ylim=c(0,500),main=sprintf('Posterior, exact likelihood\nmean=%.2f sd=%.2f\n95%% interval=[%0.f,%0.f]  (Wright: [1,42])',mean(pars_sample),sd(pars_sample),q[1],q[2]))

# se invece si e` ignoranti in matematica come lo sono io... con likelihood simulata, è forse questo un esempio di `modello generativo`?
dimensione_della_popolazione <- 100
dimensione_del_campione <- 10
difettosi_nel_campione <-c(1)
difettosi_nella_popolazione <- seq(0,dimensione_della_popolazione,by=1)
pars <- expand.grid(difettosi_nella_popolazione=difettosi_nella_popolazione)

my_likelihood <- function(a,wb,bb,n)
{
  sz <- 10e3
  urn <- c(rep('b',bb),rep('w',wb))
  cnt <- 0
  for(i in 1:sz){
    cnt = cnt+(sum(sample(urn,n,replace=FALSE)=='w')==a)
  }
  cnt/sz
}

pars$difettosi_nella_popolazione_prior <- dunif(pars$difettosi_nella_popolazione,0,dimensione_della_popolazione)
#pars$difettosi_nella_popolazione_prior <- dnorm(pars$difettosi_nella_popolazione,10,1)
pars$prior <- pars$difettosi_nella_popolazione_prior
for (i in 1:nrow(pars)) {
  likelihoods <- my_likelihood(difettosi_nel_campione,pars$difettosi_nella_popolazione[i],dimensione_della_popolazione-pars$difettosi_nella_popolazione[i],dimensione_del_campione)
  pars$likelihood[i] <- prod(likelihoods)
}
pars$unnormalized_posterior <- pars$likelihood*pars$prior
pars$posterior <- pars$unnormalized_posterior/sum(pars$unnormalized_posterior)

sample_indices <- sample(1:nrow(pars), size=1e4, replace = TRUE, prob=pars$posterior)
pars_sample <- pars[sample_indices,'difettosi_nella_popolazione']
print(head(pars_sample))

print(mean(pars_sample))
print(sd(pars_sample))
q = quantile(pars_sample,c(0.025,0.975))
print(q)

hist(pars_sample,breaks=difettosi_nella_popolazione-.5,freq=TRUE,ylim=c(0,500),main=sprintf('Posterior, simulated likelihood\nmean=%.2f sd=%.2f\n95%% interval=[%0.f,%0.f] (Wright: [1,42])',mean(pars_sample),sd(pars_sample),q[1],q[2]))
