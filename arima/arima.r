library("forecast")
data <- read.csv('data.csv',sep=',',header=FALSE)
data <- as.matrix(data)
print(dim(data))#shape
rst <- data[,1:2]
rst <- cbind(rst,0)#add a column as preds
colnames(rst)<-c("item_id", "store_id", "pred")

for(i in 1:dim(data)[1]){
  print(i)
  v <- rev(data[i,3:32])#remember to reverse
  v <- ts(as.numeric(v))
  fit <- auto.arima(v)
  plot(forecast(fit,h=1))
  pred <- forecast(fit,h=1)
  rst[i,3] <- sum(as.numeric(pred[["mean"]]))
  
}

write.csv(rst,'test.csv',quote = FALSE,row.names = FALSE,fileEncoding = "utf8")