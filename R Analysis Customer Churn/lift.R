library(ROCR)
gain.chart <- function(df) {
  score <- runif(df)
  y <- (runif(df) < score)
  plot(performance(prediction(score, y), 'tpr', 'rpp'),
       lwd = 7, main = paste('N =', df))
  lines(ecdf((rank(-score)[y == T]) / df),
        verticals = T, do.points = F, col = 'red', lwd = 3)
}

set.seed(1)
par(mfrow = c(1, 2))
gain.chart(10)
gain.chart(10000)

Var <- df$churn/df
summary(Var)
scale(Var)
