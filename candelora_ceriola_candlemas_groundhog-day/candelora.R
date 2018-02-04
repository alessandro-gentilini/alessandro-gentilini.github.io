# Get the data from https://mesonet.agron.iastate.edu/request/download.phtml?network=IT__ASOS
df <- read.csv('asos.txt',header = TRUE,sep=',',skip = 5,na.strings = "M")
df$timestamp <- strptime(df$valid,"%Y-%m-%d %H:%M")

require(lubridate)
years <- c()
candelora_CAVOK_percentage <- c()
following_month_CAVOK_percentage <-c()
station <- c()
for(y in min(year(df$timestamp)):max(year(df$timestamp))){
  years <- c(years,y)
  id<-"LIPE"
  station <- c(station,id)
  candelora <- df[df$station==id & month(df$timestamp)==2 & day(df$timestamp)==2 & year(df$timestamp)==y,]
  following_month <- df[df$station==id & ymd(sprintf("%d0203",y))<df$timestamp & df$timestamp<ymd(sprintf("%d0303",y)),]
  candelora_CAVOK_percentage <- c(candelora_CAVOK_percentage, 100*sum(grepl('CAVOK',candelora$metar))/nrow(candelora))
  following_month_CAVOK_percentage <- c(following_month_CAVOK_percentage, 100*sum(grepl('CAVOK',following_month$metar))/nrow(following_month))
}
result <- data.frame(station=station,year=years,candelora_CAVOK_percentage=candelora_CAVOK_percentage,following_month_CAVOK_percentage=following_month_CAVOK_percentage)

