# Including required libraries for first  
library(rio) # rio lib is used for reading dta files
library(cem)
data <-import ("C:/Users/Aleson/Desktop/appelloyle_jprdata.dta")

# Making a replication of dataset

df <- data



par(mar=c(1,1,1,1))

# Making a matrix of our independent variable 

mat= c(df$v3Mdiff)
barplot(mat,df$v3Mdiff, main="Plot") #Then simply plot 

# Applying regression on independent variable

test <- lm(df$v3Mdiff ~., data =df)
summary(test)
plot(test)
# Finding out correlation of out dataset

rel <-cor(data.frame(df))

# Ploting histogram of correlation (Either it was not done the author this is an extension)

hist(rel)
newdata <- data

# Applying Clustering to our dataset for futher classification of out dataset

set.seed(95)
newdata <- kmeans(data[, 3:4], 3, nstart = 95)
newdata
summary(newdata)
# Making new dataset as made by author in article
dataset1 <- df$peace_agreement_lag+df$victory_lag+df$damage
hist (dataset1)

# Applying Regression and training our independent variable 

model <- lm(df$v3Mdiff ~ df$peace_agreement_lag+df$victory_lag+ df$damage)

plot(model)
# Making predictable model
predict <- predict(model, type = 'response')

# confusion matrix
table(df$v3Mdiff, predict > 0.5)

#Applying Regression and training another variable as author done. 

dataset2 <- lm(df$v2diff~., data = df)
plot(dataset2)

# Applying logistic regression

df$v3Mdiff <- factor(df$v3Mdiff)
mylogit <- glm(df$v3Mdiff ~ df$peace_agreement_lag+df$victory_lag+ df$damage, data = df, family = "binomial")
plot(mylogit)
