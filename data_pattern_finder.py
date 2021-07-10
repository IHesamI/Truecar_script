from pip._vendor import requests
from mysql import connector
from  sklearn import tree
import re
# THIS PROGRAM GET THE DATA OF CARS FROM A DATABASE AND GIVE THE BEST CAR WITH GIVEN BUDGET BY USING MACHINE LEARNING


sql_connector=connector.connect(user="root" ,password="12345678",host="localhost",database="truecar")
cursor_sql_connector=sql_connector.cursor()
cursor_sql_connector.execute("SELECT * FROM cars_of_truecar")
list_of_cars=cursor_sql_connector.fetchall()
x=[]
y=[]

for car in list_of_cars:
   x.append([float(re.sub(",","",car[4]))])
   y.append(car[0])


tree_finder=tree.DecisionTreeClassifier()
tree_finder=tree_finder.fit(x,y)


the_best_car=tree_finder.predict([[input("Enter your budget: ")]])

print("The best car you can buy with that budget is : %s"%(the_best_car[0]))
print("ALL %s in truecar"%(the_best_car[0]))
for the_car in list_of_cars:
    if the_best_car[0]==the_car[0]:
        print("Year model: %s\n Type of car: %s\n Price label: %s\n Price: %s\n Milage: %s\n Location: %s\n Colors: %s\n Condition of car: %s\n"%(the_car[1],the_car[2],the_car[3],the_car[4],the_car[5],the_car[6],the_car[7],the_car[8]))

