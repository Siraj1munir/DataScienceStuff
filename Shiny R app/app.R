## app.R ##
library(shiny)
library(shinydashboard)
library(readr)
library(rpart)
library(rpart.plot)
library(rattle)
library(RColorBrewer)
library(caret)
library(class)

ui <- dashboardPage(
    dashboardHeader(title = "Welcome"),
    ## Sidebar content
    dashboardSidebar(
      sidebarMenu(
        menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard")),
        menuItem("K Means", tabName = "K Means", icon = icon("th")),
        menuItem("Logistic Regression", tabName = "Logistic Regression", icon = icon("th")),
        menuItem("KNN", tabName = "KNN", icon = icon("th")),
        menuItem("Decision Tree", tabName = "Decision Tree", icon = icon("th"))
        
      )
      
    ),
    ## Body content
    dashboardBody(
      tabItems(
        # First tab content
        tabItem(tabName = "dashboard",
               
                  wellPanel(
                    fileInput('file1', 'Load the Bank csv file',
                              accept=c('text/csv','text/comma-separated-values,text/plain','.csv'))
                   
                    
                  )
                
        )
        
      ),
      
      # Second tab content
      tabItem(tabName = "K Means"
      ),
      # Second tab content
      tabItem(tabName = "
              Logistic Regression"      
              ),
      # Second tab content
      tabItem(tabName = "Decision Tree",
              plotOutput("tree")
      ),
      # Second tab content
      tabItem(tabName = "KNN Algorithm"
              
          
      )
    )
    )

server <- function(input, output) {
  observe({
    file1 = input$file1
    
    if (is.null(file1) ) {
      return(NULL)
    }
    bank <<- read.csv(file1$datapath)
 
  })
  
  
  
  output$tree <- renderPlot({
    inTrain <- createDataPartition(y = bank$Y,
                                   p = 0.7,
                                   list = FALSE)
    train <- bank[ inTrain,]
    test <- bank[-inTrain,]
    tree <- rpart(train$Y ~ .,
                        data = train)
    plot(tree)
  })
    
}

shinyApp(ui =ui, server= server)