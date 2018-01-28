df <- data.frame(time=c("2017-01-21T11:00","2017-01-21T12:40","2017-01-21T16:20",
                        "2017-01-21T17:45","2017-01-21T19:20","2017-01-21T23:05",
                        "2017-01-22T07:50"
)
,temperature=c(90,82,62,64,60,52,40))
df$time <- strptime(df$time, "%Y-%m-%dT%H:%M")

library(lubridate)
time_diff <- as.numeric(difftime(df$time,df$time[1],units = "secs"))
secs <- seconds_to_period(time_diff)
elapsed<-sprintf('%02d:%02d:%02d', hour(secs), minute(secs), second(secs)) 

linear_model <- lm(df$temperature~time_diff)
title <- sprintf("Perdita di calore di mezzo litro d'acqua in un termos: circa %.1f°C/ora",abs(60*60*linear_model$coefficients[2]))
plot(strptime(elapsed, "%H:%M:%S"),df$temperature,type="b",xlab="ore:minuti",ylab="°C",main=title,ylim=c(15,100))
abline(h=19,lty=2)
text(strptime(elapsed, "%H:%M:%S")[6],22,"Temperatura ambiente")

abline(a=linear_model$coefficients[2],b=linear_model$coefficients[1])