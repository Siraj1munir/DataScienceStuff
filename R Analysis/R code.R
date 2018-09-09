# Reading testing dataset provided

dataset = read.csv("C:/Users/Aleson/Desktop/jcw.csv") 
dataset1 = read.csv("C:/Users/Aleson/Desktop/jcw - Copy.csv") 

data1<-lm(empworkfe~rgpd,data=dataset)
summary(data1)
par(mfrow=c(2,2))
plot(data1)



dataset<-sample(1:20,20)+rnorm(10,sd=2)
dataset1<-dataset+rnorm(10,sd=3)
# Put datasets into dataframe and plot them
df<-data.frame(dataset , dataset1)
plot (df[,1:2])

# Finding out contingency table 
testtable <- table(df) 
testtable  
fisher.test(testtable)
#finding Corelation matrix 
cor(df,method="pearson")
cor(df[,1:2],method="spearman")
cor.test(df$dataset,df$dataset1,method="pearson")
cor.test(df$dataset,df$dataset1,method="spearman")
# Finding mean median and variance
mean(dataset)
mean(dataset1)
median(dataset)
median(dataset1)
var(dataset)
var(dataset1)


