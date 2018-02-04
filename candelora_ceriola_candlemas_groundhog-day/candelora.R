# Get the data from https://mesonet.agron.iastate.edu/request/download.phtml?network=IT__ASOS
df <- read.csv('asos.txt',header = TRUE,sep=',',skip = 5,na.strings = "M")
df$timestamp <- strptime(df$valid,"%Y-%m-%d %H:%M")

require(lubridate)

get_result <- function(station,data)
{
  years <- c()
  candelora_CAVOK_percentage <- c()
  following_month_CAVOK_percentage <-c()
  for(y in min(year(df$timestamp)):max(year(df$timestamp))){
    candelora <- df[df$station==station & month(df$timestamp)==2 & day(df$timestamp)==2 & year(df$timestamp)==y,]
    following_month <- df[df$station==station & ymd(sprintf("%d0203",y))<df$timestamp & df$timestamp<ymd(sprintf("%d0303",y)),]
    print(sprintf("%d %d %s",y,nrow(following_month),max(following_month$timestamp)))
    if(nrow(following_month)>0 & max(following_month$timestamp)>=ymd(sprintf("%d0302",y))){
      years <- c(years,y)
      candelora_CAVOK_percentage <- c(candelora_CAVOK_percentage, 100*sum(grepl('CAVOK',candelora$metar))/nrow(candelora))
      following_month_CAVOK_percentage <- c(following_month_CAVOK_percentage, 100*sum(grepl('CAVOK',following_month$metar))/nrow(following_month))
    }
  }
  result <- data.frame(year=years,candelora_CAVOK_percentage=candelora_CAVOK_percentage,following_month_CAVOK_percentage=100-following_month_CAVOK_percentage)  
}

print(get_result("LIPE",df))
print(get_result("LIPK",df))

