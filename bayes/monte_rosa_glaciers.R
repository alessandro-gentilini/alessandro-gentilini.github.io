df <- read.csv('monte_rosa_glaciers.txt')
df$km3 <- df$Estimated.water.reservoir.million.of.cubic.meter/1000
plot(df$Surface.square.km,df$km3,log="xy",
xlab='Glacier surface/km²',
ylab='Estimated water reservoir/km³',
main="Monte Rosa Glaciers (Valle d'Aosta, Italy)",
family='serif'
)
par(family = "serif")
x=seq(0,10,.1)
lines(x,.032*x^1.36,lty=2)


y <- df$km3
x <- df$Surface.square.km
m <- nls(y~a*x^b,start=c(a=1,b=1))
print(m)

a <- coef(m)[1]
b <- coef(m)[2]

lines(x,a*x^b,type='l')
legend('bottomright',
legend=c('Data from Mercalli et al., 1991','Power law fitted to data','Formula in Bahr et al., 1997'),
lty=c(NA,1,2),
pch=c(1,NA,NA)
)
text(x=1.75*df$Surface.square.km[3],y=df$km3[3],labels='Netscho IT4L01502005')