from advertools import knowledge_graph
import pandas as pd
key = 'Your KG-Key from google console'
results = knowledge_graph(key=key, query='Add query text')
test = results[['result.name',"result.@id", "result.description", "result.detailedDescription.articleBody"]]
print(test)
