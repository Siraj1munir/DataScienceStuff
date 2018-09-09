#At first load all requirerd libraries 
library(class)
library(glmnet)
library(MASS)
library(boostr)
library(mvtnorm)          
library(multinomRob )   
library(lars)
library(stats)
library(leaps)
library(care)
library(Hmisc)
library(klaR)
library(e1071) 
library(kknn)
library(rpart)

set.seed(1306)

# Loading data into my workspace.

data = read.csv("C:/Users/Aleson/Desktop/diabetes.csv")

age <- runif(50, 0, 1)
sex <- age + rnorm(50, 0, 0.25)
bmi <- (age + sex)/2 + runif(50, 0, 0.1)
map <- runif(50, 0, 1)
tc <- (2*map + rnorm(50, 0, 0.25))/2 + runif(50, 0, 0.1)
ldl <- runif(50, 0, 1)
hdl <- runif(50, 0, 1)
ltg <- runif(50, 0, 1)
tch <- runif(50, 0, 1)
glu <- runif(50, 0, 1)
y <- (3 + age + sex + 0.5*bmi + 0.75*map + 0.5*tc + 0.5*ldl + 0.5*hdl + 0.5*tch + 0.5*ltg + 0.5*glu + rnorm(50, 0, 1))



x <- scale( cbind(age,sex,bmi,map,tc,ldl,hdl,ltg,tch,glu) )
trdata <- data.frame( cbind(x,y) )
names(trdata) <- c("sage", "ssex", "sbmi", "smap", "stc", "sldl" , "shdl" , "stch" , "sltg" , "sglu" , "y")
attach(trdata)
cor(trdata)


ols1 <- lm(y ~ sage + ssex + sbmi + smap + stc + sldl + shdl + stch + sltg + sglu)
summary(ols1)

ols2 <- lm(y ~ sage + ssex + sbmi + smap + stc + sldl + shdl + stch + sltg + sglu)
summary(ols2)

ols3 <- lm(y ~ sage + ssex + sbmi + stc + sldl + shdl + stch + sltg + sglu)
summary(ols3)

ols4 <- lm(y ~ sage + sbmi + stc + sldl + shdl + stch + sltg + sglu)
summary(ols4)

ols5 <- lm(y ~ sage + stc + sldl + shdl + stch + sltg + sglu)
summary(ols5)

ols6 <- step(ols1, direction="both")
summary(ols6)

set.seed(1310)
cv.lasso <- cv.glmnet(x, y, family='binomial', alpha=1, parallel=TRUE, standardize=TRUE, type.measure='auc')

# Applying Lasso and lars 
las <- lars(x, y, type="lasso")
las
plot(las, plottype="coefficients")


plot(las, plottype="Cp")

las.coef <- predict.lars(las, type="coefficients", mode="fraction", s=1)
las.coef
ols1

plot(ols1)

lmridge <- lm.ridge(y ~ sage + ssex + sbmi + smap + stc + sldl + shdl + stch + sltg + sglu, lambda = seq(0, 10, 1))
lmridge$kHKB
lmridge$kLW
lmridge$GCV


lmridge <- lm.ridge(y ~ sage + ssex + sbmi + smap + stc + sldl + shdl + stch + sltg + sglu, lambda = seq(6.72, 6.84, 0.01))
lmridge$GCV


# Evaluating ridge regression

ridge1 <- lm.ridge(y ~ sage + ssex + sbmi + smap + stc + sldl + shdl + stch + sltg + sglu, lambda = 2.7)
ridge2 <- lm.ridge(y ~ sage + ssex + sbmi + smap + stc + sldl + shdl + stch + sltg + sglu, lambda = 4.0)
ridge3 <- lm.ridge(y ~ sage + ssex + sbmi + smap + stc + sldl + shdl + stch + sltg + sglu, lambda = 6.8)
ridge4 <- lm.ridge(y ~ sage + ssex + sbmi + smap + stc + sldl + shdl + stch + sltg + sglu, lambda = 0)

ols1
ridge4$coef

pcomp.tr
plot(pcomp.tr)

pc1 <- pcomp.tr[,1]
pc2 <- pcomp.tr[,2]
pc3 <- pcomp.tr[,3]
pc4 <- pcomp.tr[,4]
pc5 <- pcomp.tr[,5]
pc6 <- pcomp.tr[,6]

pcr1 <- lm(y ~ pc1 + pc2 + pc3 + pc4 + pc5 + pc6)
summary(pcr1)
plot(pcr1)

# I'm using backward elimination on my data.
pcr2 <- lm(y ~ pc1 + pc2 + pc4 + pc5 + pc6 )
summary(pcr2)
plot(pcr2)
pcr3 <- lm(y ~ pc1 + pc2 + pc4 + pc6)
summary(pcr3)
plot(pcr3)
pcr4 <- lm(y ~ pc1 + pc2 + pc4)
summary(pcr4)
plot(pcr4)
pcr5 <- step(pcr1)
summary(pcr5)
plot(pcr5)

gage <- runif(5000, 0, 1)
gsex <- gage + rnorm(5000, 0, 0.25)
gbmi <- (gage + gsex)/2 + runif(5000, 0, 0.1)
gmap <- runif(5000, 0, 1)
gtc <- (2*gmap + rnorm(5000, 0, 0.25))/2 + runif(5000, 0, 0.1)
gldl <- runif(5000, 0, 1)
ghdl <- runif(5000, 0, 1)
gtch <- runif(5000, 0, 1)
gltg <- runif(5000, 0, 1)
gglu <- runif(5000, 0, 1)
gy <- (3 + gage + gsex + 0.5*gbmi + 0.75*gmap + 0.5*gtc + 0.5*gldl + 0.5*ghdl + 0.5*gtch + 0.5*gltg + 0.5*gglu  + rnorm(5000, 0, 1))

plot(gy)

sgage <- (gage - mean(age))/sqrt(var(age))
sgsex <- (gsex - mean(sex))/sqrt(var(sex))
sgbmi <- (gbmi - mean(bmi))/sqrt(var(bmi))
sgmap <- (gmap - mean(map))/sqrt(var(map))
sgtc <- (gtc - mean(tc))/sqrt(var(tc))
sgldl <- (gldl - mean(ldl))/sqrt(var(ldl))
sghdl <- (ghdl - mean(hdl))/sqrt(var(hdl))
sgtch <- (gtch - mean(tch))/sqrt(var(tch))
sgltg <- (ltg - mean(ltg))/sqrt(var(ltg))
sgglu <- (glu - mean(glu))/sqrt(var(glu))

# Binding dataset

gx <- cbind(sgage,sgsex,sgbmi,sgmap,sgtc,sgldl,sghdl,sgtch,sgltg,sgglu)
gendata <- data.frame( cbind(gx, gy) )
names(gendata) <- c("sage", "ssex", "sbmi", "smap", "stc", "sldl", "stch" , "sltg"  , "sglu",  "y")
detach(trdata)
attach(gendata)


pcomp.gen <- predict(tr.pca, newdata=gendata)
cor(pcomp.gen)


las1.mspe <- mean( (gy - predlas$fit)^2 )  
predlas <- predict.lars(las, newx=gx, type="fit", mode="fraction", s=0.56)
las2.mspe <- mean( (gy - predlas$fit)^2 )  
predlas <- predict.lars(las, newx=gx, type="fit", mode="fraction", s=1)
las3.mspe <- mean( (gy - predlas$fit)^2 )  


ridge1.mspe <- mean( (gy - (gx %*% ridge1$coef + ridge1$ym))^2 )
ridge2.mspe <- mean( (gy - (gx %*% ridge2$coef + ridge2$ym))^2 )
ridge3.mspe <- mean( (gy - (gx %*% ridge3$coef + ridge3$ym))^2 )
ridge4.mspe <- mean( (gy - (gx %*% ridge4$coef + ridge4$ym))^2 )


genpcdata <- data.frame(pcomp.gen)
names(genpcdata) <- c("pc1", "pc2", "pc3", "pc4", "pc5", "pc6", "pc7" , "pc8" , "pc9" , "pc10")
detach(gendata)
attach(genpcdata)
pcr1.mspe <- mean( (gy - predict(pcr1, newdata=genpcdata))^2 )
pcr4.mspe <- mean( (gy - predict(pcr4, newdata=genpcdata))^2 )



las1.mspe

las3.mspe

pcr1.mspe

ols1.mspe

ols5.mspe

pcr4.mspe

ridge1.mspe

ridge2.mspe

ridge3.mspe

ridge4.mspe
