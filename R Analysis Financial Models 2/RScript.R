# Loading basic library for reading dataset
library(rio)
library(ggplot2)

dataset <-import ("C:/Users/Aleson/Desktop/mansfield_data.dta")

# making a replica of dataset

frame <-dataset
par(mar=c(1,1,1,1))

# Making matrix of out independent variable

matrix = c(frame$tradescaleN)

# Plot dataset and matrix 

barplot(matrix,frame$female, main="Chart")
#models implementation

# Model 1 training  our independent variable same as done by the author
test <- lm(frame$female~., data = frame)
summary(test)
plot(test)

# Model 2 training  another variable same as done by the author

test1 <- lm(frame$tradescaleN~., data = frame)
summary(test1)
plot(test1)


# Model 3 training  another variable same as done by the author

test2 <- lm(frame$a_wage_o~.,data = frame)
summary(test2)
plot(test2)


# Model 3 training  another variable same as done by the author

test3 <- lm(frame$ln_iorient06oV2~., data = frame)
summary(test3)
plot (test3)


# Model 4 training  another variable same as done by the author

test4 <- lm(frame$ln_xorient06oV2~., data = frame)
summary(test4)
plot (test4)


# Model 5 training  another variable same as done by the author

test5 <- lm(frame$gradI~., data = frame)
summary(test5)
plot (test5)


# Model 6 training  another variable same as done by the author

test6 <- lm(frame$age~., data = frame)
summary(test6)
plot (test6)

# Making corelation  

frame1 <- cor(data.frame(dataset))
hist(frame1)

# Z-Score implementation
scale(frame, center = TRUE, scale = TRUE)

plot(scale)

# K-means
set.seed(1000)
ndata <- kmeans(frame[, 1:2], 6, nstart = 1000)
ndata
summary(ndata)

# modeling a model against dependent variables
model <- lm(frame$female ~frame$age+frame$a_wage_o+frame$ln_iorient06oV2+frame$ln_xorient06oV2+frame$incomeV3+ frame$unempB+ frame$gradI, data = frame)
summary(model)
plot(model)
# BP test
lmtest::bptest(model)
# NCV Test
car::ncvTest(model)
# GM Rule
problem <- function(dAll,nreps,name,sampleSize=10) {
  xAll <- matrix(data=c(dAll$x0,dAll$x1),ncol=2)
  cAll <- solve(t(xAll) %*% xAll) %*% t(xAll)
  beta <- as.numeric(cAll %*% dAll$y)
  
  betaSamples <- matrix(data=0,nrow=2,ncol=nreps)
  nrows <- dim(dAll)[[1]]
  for(i in 1:nreps) {
    dSample <- dAll[sample.int(nrows,sampleSize,replace=TRUE),]
    individualError <- rnorm(sampleSize)
    dSample$y <- dSample$y + individualError
    dSample$e <- dSample$z + individualError
    xSample <- matrix(data=c(dSample$x0,dSample$x1),ncol=2)
    cSample <- solve(t(xSample) %*% xSample) %*% t(xSample)
    betaS <- as.numeric(cSample %*% dSample$y)
    betaSamples[,i] <- betaS
  }
  d <- c()
  for(i in 1:(dim(betaSamples)[[1]])) {
    coef <- paste('GM',(i-1),sep='')
    mean <- mean(betaSamples[i,])
    dev <- sqrt(var(betaSamples[i,])/nreps)
    d <- rbind(d,data.frame(GMModel=nreps,model=name,coef=coef,
                            actual=beta[i],est=mean,estP=mean+2*dev,estM=mean-2*dev))
  }
  d
}

repCounts <- as.integer(floor(10^(0.25*(4:24))))
set.seed(2000)
Good_data <- data.frame(x0=1,x1=0:10)
Good_data$y <- 3*Good_data$x0 + 2*Good_data$x1
Good_data$z <- Good_data$y - predict(lm(y~0+x0+x1,data=Good_data))
print(Good_data)
Good_pos <- c()
set.seed(2000)
for(reps in repCounts) {
  Good_pos <- rbind(Good_pos,problem(Good_data,reps,'goodData'))
}
ggplot(data=Good_pos,aes(x= GMModel)) + geom_line(aes(y=actual)) + geom_line(aes(y=est),linetype=2,color='red') + geom_ribbon(aes(ymax=estP,ymin=estM),alpha=0.2,fill='green') + facet_wrap(~coef,ncol=1,scales='free_y') + scale_x_log10() + theme(axis.title.y=element_blank())

