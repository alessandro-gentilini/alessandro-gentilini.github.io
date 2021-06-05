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
lines(x,.032*x^1.36)
legend('bottomright',
legend=c('Mercalli et al., 1991','Formula in Bahr et al., 1997'),
lty=c(NA,1),
pch=c(1,NA)
)

