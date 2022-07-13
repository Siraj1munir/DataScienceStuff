import py2neo
from py2neo import Graph
import re as re
import random as random

# Main Code
play = True
while play:
    print("Welcome to the Semantic HYPFS!")
    response= input("Please enter your query. \n Choose 1 for OLC search. \n Choose 2 for CID search. \n Choose 3 for Person search.\n Choose 4 for Location search. \n Choose 5 for RFID search. \n Your Choice:" )
    if response == "1":
        OLC = input("Enter Your Desired OLC:")
        if re.match(r'^[A-Za-z{+}0-9]{7}$', OLC):
            def get_data(OLC):
                graph = Graph("bolt://localhost:7687", auth=("neo4j", "123"))
                query = """
                MATCH (OLC:OLC {{Code: '{code}'}}),p=(OLC)-[r:OLC_HAS_CID]->() RETURN p """.format(code = OLC)
                data = graph.run(query).data()
                print(data)
                return data
            get_data(OLC)
        else:
            print("Invalid OLC")
    elif response == "2":
        CID = input("Enter Your Desired CID:")
        if re.match(r'^[A-Za-z0-9]{46}$', CID):
            def get_data(CID):
                graph = Graph("bolt://localhost:7687", auth=("neo4j", "123"))
                query = """
                    MATCH (n:C_ID {{value: '{value}'}}) RETURN n 
                    """.format(value = CID)
                data = graph.run(query).data()
                print(data)
                return data
            get_data(CID)
        else:
            print("Invalid CID")
    elif response =="3":
        Person= input("Enter Your Desired Person:")
        def get_data(Person):
            graph = Graph("bolt://localhost:7687", auth=("neo4j", "123"))
            query = """
            MATCH (n:Person {{Name: '{name}'}}), p=(n)-[r:LOCATED_AT]->() RETURN p 
            """.format(name = Person)
            data = graph.run(query).data()
            print(data)
            return data
        get_data(Person)
    elif response =="4":
        Location= input("Enter Your Desired Location:")
        def get_data(Location):
            graph = Graph("bolt://localhost:7687", auth=("neo4j", "123"))
            query = """
            MATCH (n:Location {{Name: '{name}'}}), p=(n)-[r:HAS_OLC]->() RETURN p 
            """.format(name = Location)
            data = graph.run(query).data()
            print(data)
            return data
        get_data(Person)    
    elif response =="5":
        tag= input("Enter Your RFID Tag No:")
        def get_data(tag):
            graph = Graph("bolt://localhost:7687", auth=("neo4j", "123"))
            query = """
            MATCH (n:RFID {{Tag: '{tag}'}}), p=(n)-[r:HAS_C_ID]->() RETURN p 
            """.format(tag = tag)
            data = graph.run(query).data()
            print(data)
            return data
        get_data(tag)    
    else:
        print("Invalid Response Code!")    
    while play == True:
        print("Would you like to search more? (y/n)")
        answer =  input()
        if answer == 'y':
            play = True
            print("Cool! Choose your option!")
            break
        else:
            play = False
            greetings_bye = ["See you next time!", "See Yah!", "Bye bye!", "Keep on being you!"]
            print(random.choice(greetings_bye))
            break