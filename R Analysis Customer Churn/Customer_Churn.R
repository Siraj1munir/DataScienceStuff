
my.env <- environment()
Data <- load('C:/Users/Siraj/Desktop/Cell2Cell.RData', envir = my.env)

df <- data.frame(my.env$cell2cell_DF, stringsAsFactors=FALSE)

model1 <- lm(df$churn ~., data= df)
summary(model1)
plot(model1)
cor(df[,1:69],method="spearman")
Model <- glm(df$churn ~ df$customer+ df$validation+ df$revenue+df$mou+df$recchrge+df$directas+df$overage+df$roam+df$changem+df$changer+df$dropvce+df$dropvce+df$blckvce+df$unansvce+df$custcare+df$threeway+df$mourec+df$outcalls+df$incalls+df$peakvce+df$dropblk+df$callfwdv+df$callwait+df$months+df$uniqsubs+df$actvsubs+df$phones+df$models+df$eqpdays+df$age1+df$age2+df$children+df$credita+df$creditaa+df$prizmrur+df$prizmub+df$prizmtwn+df$refurb+df$webcap+df$truck+df$rv+df$occprof+df$occcler+df$occcrft+df$occstud+df$occhmkr+df$occret+df$occself+df$ownrent+df$marryun+df$marryyes+df$mailord+df$mailres+df$mailflag+df$travel+df$pcown+df$creditcd+df$retcalls+df$retaccpt+df$newcelly+df$newcelln+df$refer+df$incmiss+df$income+df$mcycle+df$setprcm+df$setprc+df$retcall, data = my.env) 
summary(Model)
fitted.values(Model)
plot(Model)

train <- df 
test <- Data
head(train)
randomSeed = 1337
set.seed(randomSeed)
LogLossBinary = function(actual, predicted, eps = 1e-15) {  
  predicted = pmin(pmax(predicted, eps), 1-eps)  
  - (sum(actual * log(predicted) + (1 - actual) * log(1 - predicted))) / length(actual)
}
library(gbm)
gbmModel = gbm(formula = df$churn ~ df$validation,
               distribution = "bernoulli",
               data = train,
               n.trees = 2500,
               shrinkage = .01,
               n.minobsinnode = 20)
gbmTrainPredictions = predict(object = gbmModel,
                              newdata = train,
                              n.trees = 1500,
                              type = "response")
head(data.frame("Actual" = train$churn, 
                "PredictedProbability" = gbmTrainPredictions))
LogLossBinary(train$churn, gbmTrainPredictions)
dataSubsetProportion = .2
randomRows = sample(1:nrow(train), floor(nrow(train) * dataSubsetProportion))
trainingHoldoutSet = train[randomRows, ]
trainingNonHoldoutSet = train[!(1:nrow(train) %in% randomRows), ]
trainingHoldoutSet$RowID = NULL
trainingNonHoldoutSet$RowID = NULL
trainingHoldoutSet$Model = NULL
trainingNonHoldoutSet$Model = NULL
gbmForTesting = gbm(formula = df$churn ~ df$validation+df$revenue,
                    distribution = "bernoulli",
                    data = trainingNonHoldoutSet,
                    n.trees = 1500,
                    shrinkage = .01,
                    n.minobsinnode = 50)
summary(gbmForTesting, plot = FALSE)
gbmHoldoutPredictions = predict(object = gbmForTesting,
                                newdata = trainingHoldoutSet,
                                n.trees = 100,
                                type = "response")

gbmNonHoldoutPredictions = predict(object = gbmForTesting,
                                   newdata = trainingNonHoldoutSet,
                                   n.trees = 100,
                                   type = "response")
print(paste(LogLossBinary(train$churn[randomRows], gbmHoldoutPredictions), 
            "Holdout Log Loss"))
print(paste(LogLossBinary(train$churn[!(1:nrow(train) %in% randomRows)], gbmNonHoldoutPredictions), 
            "Non-Holdout Log Loss"))
