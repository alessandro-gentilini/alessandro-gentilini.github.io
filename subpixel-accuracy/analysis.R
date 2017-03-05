pdf("R_plot_%d.pdf")
df<-readr::read_csv('data.csv')
for(i in seq(1,nrow(df))){
	if(is.na(df$value[i])){
		df$value[i]=df$num[i]/df$den[i]
	}
}

library(ggplot2)

plot(ggplot(data=df)
	+geom_point(aes(x=year,y=value))
	+scale_y_continuous(trans="log10",breaks=c(0.001,df$value))
	+ylab('Accuracy in pixel (log scale)'))

