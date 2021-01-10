# wb+bb dimensione popolazione
wb <- 10 # white ball
bb <- 90 # black ball
n <- 7   # dimensione campione
a <- 3   # il numero di white ball trovate nel campione

print(sprintf('prob esatta di trovare %0.f bianche',wb))
print(sprintf('in un campione di dimensione %0.f', n))
print(sprintf('estratto senza rimpiazzo da una popolazione'))
print(sprintf('composta da %0.f bianche e %0.f nere: %f',wb,bb,dhyper(a,wb,bb,n)))

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

print(sprintf('La stessa prob stimata con una simulazione: %f',my_likelihood(a,wb,bb,n)))

